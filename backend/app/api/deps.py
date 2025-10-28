from typing import Callable, Sequence
from fastapi import Depends, HTTPException
from app.repositories.auth_repository import get_current_user


def require_roles(*allowed_roles: Sequence[str]) -> Callable:
    """
    Dependency factory to require one of the allowed roles.

    Usage in a route:
        @router.get(...)
        def endpoint(current_user=Depends(require_roles("admin", "manager"))):
            ...
    """

    def _dependency(current_user = Depends(get_current_user)):
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Support current_user as dict (from user repository) or object with attribute `role`
        if isinstance(current_user, dict):
            role = current_user.get("role")
        else:
            role = getattr(current_user, "role", None)

        if role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        return current_user

    return _dependency
