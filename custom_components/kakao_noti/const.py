"""Constants for the Kakao Notify integration.

All runtime defaults are hardcoded here. The config flow does not expose
these as user options — the integration is install-and-go.
"""
from __future__ import annotations

DOMAIN = "kakao_noti"

# Hardcoded runtime defaults (no user-facing config)
DEFAULT_SERVICE_NAME = "kakao_noti"
DEFAULT_TIMEOUT = 10
DEFAULT_MAX_LEN = 1850
DEFAULT_LINK_WEB_URL = "https://www.kakao.com"

# Kakao OAuth / API endpoints
KAKAO_AUTHORIZE_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_MEMO_SEND_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"
KAKAO_SCOPE = "talk_message"

# Entry data keys
CONF_SERVICE_NAME = "service_name"
CONF_KAKAO_USER_ID = "kakao_user_id"
CONF_NICKNAME = "nickname"

TRUNCATE_SUFFIX = "\n… (이하 생략)"
