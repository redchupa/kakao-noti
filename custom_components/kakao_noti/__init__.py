"""Kakao Notify integration — HA-native OAuth2 + NotifyEntity (multi-account)."""
from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.service import async_set_service_schema

from .api import KakaoAPI, fetch_kakao_user_info
from .const import (
    CONF_KAKAO_USER_ID,
    CONF_NICKNAME,
    CONF_SERVICE_NAME,
    DEFAULT_MAX_LEN,
    DEFAULT_SERVICE_NAME,
    DEFAULT_TIMEOUT,
    DOMAIN,
)
from .notify import truncate

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.NOTIFY]

LEGACY_SERVICE_SCHEMA = vol.Schema(
    {
        vol.Required("message"): vol.Any(str, vol.Coerce(str)),
        vol.Optional("title"): vol.Any(str, vol.Coerce(str)),
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    implementation = (
        await config_entry_oauth2_flow.async_get_config_entry_implementation(
            hass, entry
        )
    )
    session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)
    try:
        await session.async_ensure_token_valid()
    except Exception as err:  # noqa: BLE001
        _LOGGER.error("kakao_noti: 토큰 검증 실패 → 통합 재추가 필요: %s", err)
        raise

    # Migrate v0.4 → v0.5+: backfill kakao_user_id, nickname, service_name
    if not entry.data.get(CONF_KAKAO_USER_ID):
        try:
            access_token = session.token["access_token"]
            info = await fetch_kakao_user_info(hass, access_token, DEFAULT_TIMEOUT)
            user_id = str(info["id"])
            nickname = (
                info.get("kakao_account", {}).get("profile", {}).get("nickname", "")
                or info.get("properties", {}).get("nickname", "")
            )
            new_data = {
                **entry.data,
                CONF_KAKAO_USER_ID: user_id,
                CONF_NICKNAME: nickname,
                CONF_SERVICE_NAME: entry.data.get(
                    CONF_SERVICE_NAME, DEFAULT_SERVICE_NAME
                ),
            }
            hass.config_entries.async_update_entry(
                entry, data=new_data, unique_id=user_id
            )
            _LOGGER.info(
                "kakao_noti: 마이그레이션 완료 (user_id=%s, nickname=%s)",
                user_id,
                nickname,
            )
        except Exception as err:  # noqa: BLE001
            _LOGGER.warning(
                "kakao_noti: 마이그레이션 실패(무시): %s. 기존 entry는 그대로 동작.",
                err,
            )

    api = KakaoAPI(hass, entry, session)
    service_name = entry.data.get(CONF_SERVICE_NAME, DEFAULT_SERVICE_NAME)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "api": api,
        "session": session,
        "service_name": service_name,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _register_legacy_service(hass, entry, api, service_name)
    return True


def _register_legacy_service(
    hass: HomeAssistant,
    entry: ConfigEntry,
    api: KakaoAPI,
    service_name: str,
) -> None:
    """Register `notify.<service_name>` with full UI schema for GUI editor."""

    async def _handle(call: ServiceCall) -> None:
        message = call.data.get("message", "")
        title = call.data.get("title")
        body = f"[{title}]\n{message}" if title else message
        await api.send_memo(truncate(body, DEFAULT_MAX_LEN))

    hass.services.async_register(
        "notify", service_name, _handle, schema=LEGACY_SERVICE_SCHEMA
    )

    # Make the service show fields in the Developer Tools UI editor
    nickname = entry.data.get(CONF_NICKNAME, "")
    title_suffix = f" — {nickname}" if nickname else ""
    async_set_service_schema(
        hass,
        "notify",
        service_name,
        {
            "name": f"Kakao 카카오톡 나에게 보내기{title_suffix}",
            "description": (
                "카카오톡 '나와의 채팅' 으로 메시지를 발송합니다. "
                "1850자 초과 시 자동 절단됩니다."
            ),
            "fields": {
                "message": {
                    "name": "Message",
                    "description": "본문 텍스트. 멀티라인 지원.",
                    "required": True,
                    "example": "현관문이 열렸어요",
                    "selector": {"text": {"multiline": True}},
                },
                "title": {
                    "name": "Title",
                    "description": "선택 — 본문 앞에 [제목]\\n 으로 prefix 됩니다.",
                    "required": False,
                    "example": "도어센서",
                    "selector": {"text": {}},
                },
            },
        },
    )

    entry.async_on_unload(
        lambda: hass.services.async_remove("notify", service_name)
    )


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return unloaded
