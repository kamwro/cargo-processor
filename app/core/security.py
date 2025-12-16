from fastapi import Depends, Header, HTTPException, status

from .config import get_settings


API_KEY_HEADER = "X-Cargo-Api-Key"


async def require_api_key(
    x_cargo_api_key: str | None = Header(default=None, alias=API_KEY_HEADER),
    settings=Depends(get_settings),
) -> None:
    expected = settings.api_key
    if expected is None:
        # Allow in dev when API_KEY is not set
        return
    if x_cargo_api_key != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
