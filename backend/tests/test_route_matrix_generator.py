"""Sanity checks for the route-matrix generator after router nesting changes."""

from generate_route_matrix import build_rows, render


def test_generated_paths_keep_api_prefix():
    rows = build_rows()
    api_rows = [row for row in rows if row[1].startswith("/api/v1/")]
    assert len(api_rows) > 800

    other_paths = {row[1] for row in rows if not row[1].startswith("/api/v1/")}
    assert other_paths <= {"/", "/health", "/docs/oauth2-redirect"}

    # Regression guard: nested routers must not lose the mounted /api/v1 prefix.
    assert not any(row[1].startswith("/api/") and not row[1].startswith("/api/v1/") for row in rows)


def test_generator_flags_routes():
    rows = build_rows()
    flagged = [row for row in rows if row[4] != "-"]
    assert len(flagged) > 0

    content, flagged_count, unreviewed_count = render(rows)
    assert flagged_count == len(flagged)
    assert unreviewed_count == 0
    assert f"{flagged_count} of {len(rows)} routes are flagged" in content


def test_known_routes_classify_correctly():
    rows = build_rows()

    login = [row for row in rows if row[1] == "/api/v1/auth/login" and row[0] == "POST"]
    assert login and all(row[2] == "public" for row in login)

    payroll = [row for row in rows if row[1] == "/api/v1/payroll/runs" and row[0] == "GET"]
    assert payroll
    for row in payroll:
        assert "RequirePermission" in row[2]
        assert "payroll_view" in row[3]
        assert row[4] == "-"
