"""Application credentials platform — Kakao OAuth2 endpoints."""
from __future__ import annotations

from homeassistant.components.application_credentials import AuthorizationServer
from homeassistant.core import HomeAssistant

from .const import KAKAO_AUTHORIZE_URL, KAKAO_TOKEN_URL


async def async_get_authorization_server(hass: HomeAssistant) -> AuthorizationServer:
    """Return Kakao OAuth2 authorization & token URLs."""
    return AuthorizationServer(
        authorize_url=KAKAO_AUTHORIZE_URL,
        token_url=KAKAO_TOKEN_URL,
    )


async def async_get_description_placeholders(hass: HomeAssistant) -> dict[str, str]:
    """Strings shown on the application credentials add-credentials UI."""
    return {
        "more_info_url": "https://developers.kakao.com",
        "redirect_url": (
            "Add this Redirect URI in Kakao Developers console:\n"
            "<HA base URL>/auth/external/callback"
        ),
    }
