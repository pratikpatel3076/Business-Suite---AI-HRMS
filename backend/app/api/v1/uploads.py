"""Authenticated delivery of uploaded files.

The old public ``/uploads`` StaticFiles mount exposed every stored document to
unauthenticated callers. All stored URLs remain ``/uploads/<relative path>``
for database compatibility, but they are now served through this router at
``/api/v1/uploads/<relative path>`` and require an authenticated user.
"""

from __future__ import annotations

import mimetypes
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.deps import get_current_user_for_asset
from app.models.user import User

router = APIRouter(prefix="/uploads", tags=["Uploads"])

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")


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


@router.get("/{file_path:path}")
def download_upload(
    file_path: str,
    _current_user: User = Depends(get_current_user_for_asset),
) -> FileResponse:
    path = _safe_upload_path(file_path)
    media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return FileResponse(path, media_type=media_type)
