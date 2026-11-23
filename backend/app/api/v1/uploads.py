"""Authenticated delivery of uploaded files.

The old public ``/uploads`` StaticFiles mount exposed every stored document to
unauthenticated callers. All stored URLs remain ``/uploads/<relative path>``
for database compatibility, but they are now served through this router at
``/api/v1/uploads/<relative path>`` and require an authenticated user.
"""

from __future__ import annotations

import mimetypes
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.asset_urls import ASSET_URL_TTL_SECONDS, create_signed_asset_url, verify_signed_asset_url
from app.core.config import settings
from app.core.deps import get_current_user, get_current_user_for_asset, get_db
from app.core.upload_auth import authorize_upload_access
from app.models.user import User

router = APIRouter(prefix="/uploads", tags=["Uploads"])

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
INVALID_SIGNED_URL = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired asset URL")


class AssetSignRequest(BaseModel):
    path: str


def _safe_upload_path(relative_path: str) -> Path:
    """Resolve a stored upload URL inside UPLOAD_DIR without escaping it."""
    root = Path(settings.UPLOAD_DIR).resolve()
    candidate = Path(relative_path)

    # Absolute paths and parent traversals are never legitimate stored URLs.
    if candidate.is_absolute() or ".." in candidate.parts:
        raise NOT_FOUND

    current = root
    for part in candidate.parts:
        if part in ("", "."):
            continue
        current = current / part
        # Reject symlinks at every level, including the final file, so a link
        # planted inside UPLOAD_DIR cannot point outside the storage root.
        if current.is_symlink():
            raise NOT_FOUND

    try:
        current.relative_to(root)
    except ValueError:
        raise NOT_FOUND from None

    if not current.is_file():
        raise NOT_FOUND
    return current


@router.post("/sign")
def sign_asset_url(
    payload: AssetSignRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    """Issue a 60-second signed URL after the same authorization as a download."""
    raw_path = payload.path
    stored_prefix = "/uploads/"
    api_prefix = f"{settings.API_V1_STR}/uploads/"
    if raw_path.startswith(stored_prefix):
        relative_path = raw_path[len(stored_prefix) :]
    elif raw_path.startswith(api_prefix):
        relative_path = raw_path[len(api_prefix) :].split("?", 1)[0].split("#", 1)[0]
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not a stored upload URL")

    if not relative_path or any(char in relative_path for char in "?#\\"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid asset path")

    # Reuse the traversal/symlink checks and the per-prefix authorization.
    _safe_upload_path(relative_path)
    authorize_upload_access(current_user, db, relative_path)
    return {
        "url": create_signed_asset_url(relative_path),
        "expires_in": ASSET_URL_TTL_SECONDS,
    }


@router.get("/{file_path:path}")
def download_upload(
    file_path: str,
    request: Request,
    current_user: User | None = Depends(get_current_user_for_asset),
    db: Session = Depends(get_db),
) -> FileResponse:
    # Resolve first so traversal/symlink attempts stay indistinguishable from
    # a missing file, then apply the appropriate authorization.
    path = _safe_upload_path(file_path)
    if request.query_params.get("sig") is not None:
        if not verify_signed_asset_url(
            file_path,
            request.query_params.get("expires"),
            request.query_params.get("sig"),
        ):
            raise INVALID_SIGNED_URL
    else:
        authorize_upload_access(current_user, db, file_path)
    media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return FileResponse(path, media_type=media_type)
