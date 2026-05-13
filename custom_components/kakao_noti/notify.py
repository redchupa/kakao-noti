"""Kakao Notify platform — NotifyEntity per config entry."""
from __future__ import annotations

import logging

from homeassistant.components.notify import NotifyEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import KakaoAPI
from .const import (
    CONF_NICKNAME,
    CONF_SERVICE_NAME,
    DEFAULT_MAX_LEN,
    DEFAULT_SERVICE_NAME,
    DOMAIN,
    TRUNCATE_SUFFIX,
)

_LOGGER = logging.getLogger(__name__)


def truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    head_len = max(0, limit - len(TRUNCATE_SUFFIX))
    return text[:head_len] + TRUNCATE_SUFFIX


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    api: KakaoAPI = hass.data[DOMAIN][entry.entry_id]["api"]
    async_add_entities([KakaoNotifyEntity(entry, api)])


class KakaoNotifyEntity(NotifyEntity):
    """One notify entity per config entry (= per Kakao account)."""

    _attr_should_poll = False
    _attr_has_entity_name = False

    def __init__(self, entry: ConfigEntry, api: KakaoAPI) -> None:
        self._entry = entry
        self._api = api
        service_name = entry.data.get(CONF_SERVICE_NAME, DEFAULT_SERVICE_NAME)
        nickname = entry.data.get(CONF_NICKNAME, "")
        self._attr_unique_id = entry.entry_id
        self._attr_name = service_name
        self._attr_extra_state_attributes = {
            "service_name": service_name,
            "nickname": nickname,
        }

    async def async_send_message(self, message: str, title: str | None = None) -> None:
        body = f"[{title}]\n{message}" if title else message
        await self._api.send_memo(truncate(body, DEFAULT_MAX_LEN))
