"""Config flow — HA-native OAuth2 with multi-account support.

After successful OAuth we call /v2/user/me to get the Kakao user id.
- unique_id = kakao_user_id → prevents duplicate enrollment of the same account
- service_name = 'kakao_noti' for the first entry, 'kakao_noti_2', '_3'... afterwards
"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.helpers import config_entry_oauth2_flow

from .api import fetch_kakao_user_info
from .const import (
    CONF_KAKAO_USER_ID,
    CONF_NICKNAME,
    CONF_SERVICE_NAME,
    DEFAULT_SERVICE_NAME,
    DEFAULT_TIMEOUT,
    DOMAIN,
    KAKAO_SCOPE,
)

_LOGGER = logging.getLogger(__name__)


class KakaoOAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """OAuth2 flow handler — Kakao authorize → token → entry."""

    DOMAIN = DOMAIN
    VERSION = 1

    @property
    def logger(self) -> logging.Logger:
        return _LOGGER

    @property
    def extra_authorize_data(self) -> dict[str, Any]:
        return {"scope": KAKAO_SCOPE}

    async def async_oauth_create_entry(self, data: dict[str, Any]):
        """Create the config entry after fetching the Kakao user id."""
        access_token = data["token"]["access_token"]
        try:
            user_info = await fetch_kakao_user_info(
                self.hass, access_token, timeout=DEFAULT_TIMEOUT
            )
        except Exception as err:  # noqa: BLE001
            _LOGGER.error("kakao_noti: user/me 조회 실패 → %s", err)
            return self.async_abort(reason="oauth_failed")

        user_id = str(user_info["id"])
        nickname = (
            user_info.get("kakao_account", {})
            .get("profile", {})
            .get("nickname", "")
            or user_info.get("properties", {}).get("nickname", "")
        )

        await self.async_set_unique_id(user_id)
        self._abort_if_unique_id_configured()

        existing = [
            e for e in self.hass.config_entries.async_entries(DOMAIN)
            if e.source != "ignore"
        ]
        index = len(existing) + 1
        service_name = (
            DEFAULT_SERVICE_NAME if index == 1 else f"{DEFAULT_SERVICE_NAME}_{index}"
        )

        entry_data = {
            **data,
            CONF_KAKAO_USER_ID: user_id,
            CONF_NICKNAME: nickname,
            CONF_SERVICE_NAME: service_name,
        }

        title = f"카카오 알림 — {nickname}" if nickname else f"카카오 알림 ({service_name})"
        return self.async_create_entry(title=title, data=entry_data)
