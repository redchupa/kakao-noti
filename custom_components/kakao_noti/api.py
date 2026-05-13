"""Kakao API client backed by HA OAuth2Session (auto refresh)."""
from __future__ import annotations

import json
import logging
from typing import Any

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DEFAULT_LINK_WEB_URL,
    DEFAULT_TIMEOUT,
    KAKAO_MEMO_SEND_URL,
    KAKAO_USER_ME_URL,
)

_LOGGER = logging.getLogger(__name__)


async def fetch_kakao_user_info(
    hass: HomeAssistant, access_token: str, timeout: int = DEFAULT_TIMEOUT
) -> dict[str, Any]:
    """Return /v2/user/me payload. `id` is always present regardless of scopes."""
    headers = {"Authorization": f"Bearer {access_token}"}
    http = async_get_clientsession(hass)
    async with http.get(
        KAKAO_USER_ME_URL,
        headers=headers,
        timeout=aiohttp.ClientTimeout(total=timeout),
    ) as resp:
        payload = await resp.json(content_type=None)
        if resp.status != 200 or "id" not in payload:
            raise RuntimeError(
                f"kakao user/me 호출 실패 HTTP {resp.status}: {str(payload)[:200]}"
            )
        return payload


class KakaoAPI:
    """Send Kakao 'self memo' using OAuth2Session for token management."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        session: config_entry_oauth2_flow.OAuth2Session,
    ) -> None:
        self._hass = hass
        self._entry = entry
        self._session = session

    async def send_memo(self, text: str) -> None:
        await self._session.async_ensure_token_valid()
        access_token = self._session.token["access_token"]

        template_object = {
            "object_type": "text",
            "text": text,
            "link": {"web_url": DEFAULT_LINK_WEB_URL, "mobile_web_url": DEFAULT_LINK_WEB_URL},
        }
        form = {"template_object": json.dumps(template_object, ensure_ascii=False)}
        headers = {"Authorization": f"Bearer {access_token}"}

        http = async_get_clientsession(self._hass)
        try:
            async with http.post(
                KAKAO_MEMO_SEND_URL,
                headers=headers,
                data=form,
                timeout=aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT),
            ) as resp:
                body = await resp.text()
                if resp.status == 200 and '"result_code":0' in body:
                    return
                _LOGGER.warning(
                    "kakao_noti memo 전송 실패 HTTP %s body=%s", resp.status, body[:200]
                )
        except TimeoutError:
            _LOGGER.warning("kakao_noti memo 전송 타임아웃 (%ss)", DEFAULT_TIMEOUT)
        except aiohttp.ClientError as err:
            _LOGGER.warning("kakao_noti memo 전송 실패 (network): %s", err)
