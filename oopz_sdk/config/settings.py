"""Runtime configuration objects for the Oopz SDK."""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass, field
from typing import Any

from .constants import DEFAULT_HEADERS

logger = logging.getLogger(__name__)


@dataclass
class RequestConfig:
    timeout: float | tuple[float, float] = (10, 30)


@dataclass
class RetryConfig:
    max_attempts: int = 3


@dataclass
class RateLimitConfig:
    interval: float = 0.0


@dataclass
class HeartbeatConfig:
    interval: float = 10.0
    reconnect_interval: float = 2.0
    max_reconnect_interval: float = 120.0


@dataclass
class ProxyConfig:
    http: str | None = None
    https: str | None = None
    websocket: str | None = None


@dataclass
class OneBotV12Config:
    """
    OneBot v12 适配配置。

    enabled:
        是否启用 OneBot v12 适配器。

    auto_start_server:
        是否在 OopzBot.start() 时自动启动 OneBot v12 server。
        如果只是想内部调用 adapter，可以设为 False。

    host / port:
        正向 HTTP / WebSocket server 监听地址。

    access_token:
        OneBot 连接层鉴权 token。

    ws_reverse_urls:
        反向 WebSocket 地址。配置后 SDK 会主动连接这些地址。

    webhook_urls:
        HTTP webhook 地址。事件会 POST 到这些 URL。
    """

    enabled: bool = False
    auto_start_server: bool = True

    platform: str = "oopz"
    self_id: str = ""

    db_path: str | None = None

    host: str = "127.0.0.1"
    port: int = 6727

    access_token: str = ""

    enable_http: bool = True
    enable_ws: bool = True

    webhook_urls: list[str] = field(default_factory=list)

    ws_reverse_urls: list[str] = field(default_factory=list)
    ws_reverse_reconnect_interval: float = 3.0

    send_connect_event: bool = True


@dataclass
class OneBotV11Config:
    """
    OneBot v11 适配配置。

    注意：Oopz 是 area/channel 双层结构，而 v11 是 group 单层结构。
    v11 的 group_id 默认映射为 Oopz channel_id；发送群消息时建议额外传
    oopz_area_id/area/guild_id，或在 default_area 中配置默认 area。
    """

    enabled: bool = False
    auto_start_server: bool = True

    platform: str = "oopz"
    self_id: str = ""

    db_path: str | None = None

    host: str = "127.0.0.1"
    port: int = 6700

    access_token: str = ""
    secret: str = ""

    enable_http: bool = True
    enable_ws: bool = True
    enable_http_post: bool = True
    enable_ws_reverse: bool = True

    # OneBot v11 HTTP POST 事件上报地址
    http_post_urls: list[str] = field(default_factory=list)
    http_post_timeout: float = 0.0

    # OneBot v11 反向 WebSocket。
    # ws_reverse_url 表示 Universal 连接
    ws_reverse_url: str = ""
    # ws_reverse_api_url / ws_reverse_event_url 表示 API / Event 分离连接。
    ws_reverse_api_url: str = ""
    ws_reverse_event_url: str = ""
    ws_reverse_reconnect_interval: float = 3.0

    send_connect_event: bool = True

    # 因为目前的实现将area+channel作为group进行处理, 所以有些对群组的危险操作会影响整个域
    # 是否启用群组禁言被当做整个域禁言的action
    enable_area_scoped_group_ban: bool = False
    # 是否启用群组离开被当做整个域离开的action
    enable_set_group_leave_as_area_leave: bool = False
    # 是否启用群组踢人被当做整个域移除的action
    enable_set_group_kick_as_area_kick: bool = False


@dataclass
class OopzConfig:
    device_id: str
    person_uid: str
    jwt_token: str
    private_key: Any = None

    base_url: str = "https://gateway.oopz.cn"
    ws_url: str = "wss://ws.oopz.cn"
    app_version: str = "69514"
    channel: str = "Web"
    platform: str = "windows"
    web: bool = True

    use_announcement_style: bool = False

    agora_app_id: str = "358eebceadb94c2a9fd91ecd7b341602"
    agora_init_timeout: int = 1800

    voice_backend: str = "browser"
    voice_browser_headless: bool = True
    voice_browser_executable_path: str = ""
    voice_agora_sdk_url: str = "https://download.agora.io/sdk/release/AgoraRTC_N.js"

    userinfo_cache_max_entries: int = 5000
    userinfo_cache_ttl: float = 1800.0

    area_channels_cache_max_entries: int = 1000
    area_channels_cache_ttl: float = 1800.0

    person_profiles_cache_max_entries: int = 3000
    person_profile_cache_ttl: float = 1800.0

    area_user_nickname_cache_max_entries: int = 20000
    area_user_nickname_cache_ttl: float = 300.0

    area_members_page_cache_max_entries : int = 200
    area_members_page_cache_ttl: float = 10.0

    headers: dict[str, str] = field(default_factory=dict)
    retry: RetryConfig = field(default_factory=RetryConfig)
    request_config: RequestConfig = field(default_factory=RequestConfig)
    rate_limit: RateLimitConfig = field(default_factory=RateLimitConfig)
    heartbeat: HeartbeatConfig = field(default_factory=HeartbeatConfig)
    proxy: ProxyConfig = field(default_factory=ProxyConfig)

    ignore_self_messages: bool = True   # 如果设置为False, 会导致bot接收到自己处理的消息, 可能导致死循环

    auto_subscribe_joined_areas: bool = False # 加入后自动请求账号加入的所有域, 然后向websocket注册加入的域, 接受来自域的事件

    onebot_v11: OneBotV11Config = field(default_factory=OneBotV11Config)

    # todo onebot v12还未经测试, 暂时禁用
    # onebot_v12: OneBotV12Config = field(default_factory=OneBotV12Config)

    def __post_init__(self) -> None:
        self.device_id = self._require_non_empty(self.device_id, "device_id")
        self.person_uid = self._require_non_empty(self.person_uid, "person_uid")
        self.jwt_token = self._require_non_empty(self.jwt_token, "jwt_token")

        if self._is_missing_private_key(self.private_key):
            self.private_key = self._fallback_private_key()

    @staticmethod
    def _require_non_empty(value: str, field_name: str) -> str:
        text = str(value or "").strip()
        if not text:
            raise ValueError(f"{field_name} is required")
        return text

    @staticmethod
    def _is_missing_private_key(value: Any) -> bool:
        if value is None:
            return True
        if isinstance(value, str):
            return not value.strip()
        if isinstance(value, (bytes, bytearray)):
            return not value
        return False

    @staticmethod
    def _fallback_private_key() -> Any:
        from oopz_sdk.auth._builtin_login_bundle import get_client_signing_key

        logger.warning(
            "OOPZ private_key 未提供，回退到内置 client signing key。"
            "这只适合沿用已有登录态；如果后续鉴权失败，请重新登录。"
        )
        return get_client_signing_key()

    @classmethod
    def from_env(cls, prefix: str = "OOPZ_", **overrides: Any) -> "OopzConfig":
        """从环境变量创建配置。

        默认读取 `OOPZ_DEVICE_ID`、`OOPZ_PERSON_UID`、`OOPZ_JWT_TOKEN`
        和 `OOPZ_PRIVATE_KEY`。可通过关键字参数覆盖其他配置项。
        """
        values: dict[str, Any] = {
            "device_id": cls._require_env(f"{prefix}DEVICE_ID"),
            "person_uid": cls._require_env(f"{prefix}PERSON_UID"),
            "jwt_token": cls._require_env(f"{prefix}JWT_TOKEN"),
            "private_key": os.environ.get(f"{prefix}PRIVATE_KEY", ""),
        }
        app_version = os.environ.get(f"{prefix}APP_VERSION", "").strip()
        if app_version:
            values["app_version"] = app_version
        values.update(overrides)
        return cls(**values)

    @classmethod
    async def from_password(
        cls,
        phone: str,
        password: str,
        *,
        headful_env: str = "OOPZ_LOGIN_HEADFUL",
        headless: bool | None = None,
        **kwargs: Any,
    ) -> "OopzConfig":
        """使用账号密码登录并直接构造配置。"""
        from oopz_sdk.auth.password_login import login_with_password, truthy_env

        config_overrides = dict(kwargs.pop("config_overrides", {}) or {})
        if headless is None:
            headless = not truthy_env(os.environ.get(headful_env))
        credentials = await login_with_password(
            cls._require_non_empty(phone, "phone"),
            str(password or ""),
            headless=headless,
            **kwargs,
        )
        values: dict[str, Any] = {
            "device_id": credentials.device_id,
            "person_uid": credentials.person_uid,
            "jwt_token": credentials.jwt_token,
            "private_key": credentials.private_key_pem,
        }
        if credentials.app_version:
            values["app_version"] = credentials.app_version
        values.update(config_overrides)
        return cls(**values)

    @classmethod
    async def from_password_env(
        cls,
        *,
        phone_env: str = "OOPZ_LOGIN_PHONE",
        password_env: str = "OOPZ_LOGIN_PASSWORD",
        headful_env: str = "OOPZ_LOGIN_HEADFUL",
        headless: bool | None = None,
        **kwargs: Any,
    ) -> "OopzConfig":
        """用环境变量中的 OOPZ 账号密码登录并创建配置。

        默认读取 `OOPZ_LOGIN_PHONE` 和 `OOPZ_LOGIN_PASSWORD`；当 `headless`
        没有显式传入时，会按 `OOPZ_LOGIN_HEADFUL` 环境变量决定是否显示浏览器
        窗口（值为 ``1`` / ``true`` / ``yes`` / ``on`` 都会被识别为「显示窗口」）。

        `kwargs` 会传给 :func:`login_with_password`；其中 `config_overrides`
        可用于覆盖最终 ``OopzConfig`` 的字段。
        """
        return await cls.from_password(
            cls._require_env(phone_env),
            cls._require_env(password_env, strip=False),
            headful_env=headful_env,
            headless=headless,
            **kwargs,
        )

    @classmethod
    def from_password_sync(cls, phone: str, password: str, **kwargs: Any) -> "OopzConfig":
        """`from_password()` 的同步包装，适合一次性脚本。"""
        return asyncio.run(cls.from_password(phone, password, **kwargs))

    @classmethod
    def from_password_env_sync(cls, **kwargs: Any) -> "OopzConfig":
        """`from_password_env()` 的同步包装，适合一次性脚本。"""
        return asyncio.run(cls.from_password_env(**kwargs))

    @staticmethod
    def _require_env(name: str, *, strip: bool = True) -> str:
        raw = os.environ.get(name, "")
        if not raw or not raw.strip():
            raise ValueError(f"{name} environment variable is required")
        return raw.strip() if strip else raw

    @property
    def rate_limit_interval(self) -> float:
        return self.rate_limit.interval

    @rate_limit_interval.setter
    def rate_limit_interval(self, value: float) -> None:
        self.rate_limit.interval = value

    @property
    def request_timeout(self) -> float | tuple[float, float]:
        return self.request_config.timeout

    @request_timeout.setter
    def request_timeout(self, value: float | tuple[float, float]) -> None:
        self.request_config.timeout = value

    def get_headers(self) -> dict[str, str]:
        return {**DEFAULT_HEADERS, **self.headers}

