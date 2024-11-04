import asyncio
import json
from asyncio import Task
from collections import deque
from urllib.parse import urljoin

from aiogram import Bot
from aiohttp import ClientSession, FormData
from loguru import logger
from websockets import connect, WebSocketClientProtocol

from config import CONFIG
from core.interfaces import (
    StatusServer,
    StatusWS,
    SecretVisit,
    Options,
    Log,
    Slot,
)
from helpers.status_server import broadcast_server_status


class Logs:
    def __init__(self, size):
        self.size = size
        self.array = deque(maxlen=size)

    def push(self, value: Log):
        self.array.append(value)

    def __repr__(self):
        return repr(self.array)


class WebSocketFactorioZone:
    def __init__(
        self,
        url: str = CONFIG.factorio_zone.ws_url,
        log_size: int = 50,
        bot: Bot | None = None,
    ):
        self.url = url
        self.ws: WebSocketClientProtocol | None = None
        self.running = False
        self._secret_visit: SecretVisit | None = None
        self.regions: Options | None = None
        self.versions: Options | None = None
        self.saves: Options | None = None
        self._logs: Logs = Logs(size=log_size)
        self._status: StatusServer = StatusServer()
        self._slot: Slot | None = None
        self._login_data = {
            "languages": ["en-US", "en"],
            "screenHeight": 1800,
            "screenWidth": 1920,
            "timezoneOffset": -180,
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "windowHeight": 166,
            "windowWidth": 1920,
        }
        self._bot: Bot | None = bot
        self._first_init_event = True

    @property
    def visit_token(self) -> SecretVisit | None:
        return self._secret_visit

    @property
    def logs(self) -> list[Log]:
        return list(self._logs.array)

    @property
    def status(self) -> StatusWS:
        return StatusWS(
            running_ws=self.running,
            server=self._status,
            slot=self._slot,
        )

    async def keep_alive(self):
        while True:
            if self.running:
                await self.send("keepalive")
            await asyncio.sleep(10)

    async def login(self):
        await self.send(f"details {json.dumps(self._login_data)}")

    async def on_message(self, message):
        logger.info(f"WebSocketFactorioZone <- {message}")
        json_message = {}
        try:
            json_message = json.loads(message)
        except json.JSONDecodeError as _ex:
            print("JSONDecodeError", _ex)

        if json_message.get("secret"):
            self._secret_visit = SecretVisit.model_validate(json_message)

        if json_message.get("type") == "options":
            _options = Options.model_validate(json_message)
            if json_message.get("name") == "regions":
                self.regions = _options
            if json_message.get("name") == "versions":
                self.versions = _options
            if json_message.get("name") == "saves":
                self.saves = _options
        if json_message.get("line"):
            log = Log.model_validate(json_message)
            self._logs.push(log)
        if json_message.get("type") in ("running", "starting", "stopping"):
            await self._set_status(
                status=StatusServer.model_validate(json_message)
            )
        if json_message.get("type") == "slot":
            self._slot = Slot.model_validate(json_message)

    async def _set_status(self, status: StatusServer):
        logger.error(status)

        if (
            self._status.model_dump() != status.model_dump()
            and self._bot
            and not self._first_init_event
        ):
            self._status = status
            await broadcast_server_status(
                bot=self._bot,
                status=self.status,
            )
        self._status = status
        self._first_init_event = False

    async def on_error(self, error):
        logger.error(f"WebSocketFactorioZone error: {error}")

    async def on_close(self):
        logger.warning(f"WebSocketFactorioZone connection close!")
        self.running = False

    def clear_state(self):
        self._secret_visit = None
        self.regions: list[Options] | None = None
        self.versions: list[Options] | None = None
        self.saves: list[Options] | None = None
        self._status: StatusServer = StatusServer()
        self._slot: Slot | None = None

    async def on_open(self):
        logger.success(f"WebSocketFactorioZone connection open!")
        self.running = True
        await self.login()

    async def run(self):
        while True:
            try:
                async with connect(self.url) as self.ws:
                    await self.on_open()
                    try:
                        while self.running:
                            message = await self.ws.recv()
                            await self.on_message(message)
                    except Exception as e:
                        await self.on_error(e)
                    finally:
                        await self.on_close()
            except Exception as e:
                logger.error(f"WebSocketFactorioZone error connection: {e}")
                await asyncio.sleep(5)

    async def start(self):
        await self.run()

    async def send(self, message):
        if self.running and self.ws:
            logger.info(f"WebSocketFactorioZone -> `{message}`")
            await self.ws.send(message)

    async def close(self):
        self.running = False
        if self.ws:
            await self.ws.close()


class FactorioZone:
    def __init__(
        self,
        token: str,
        factorio_ws: WebSocketFactorioZone,
    ):
        self._token = token
        self.factorio_ws: WebSocketFactorioZone = factorio_ws
        self.session: ClientSession = ClientSession()
        self._ws_task: Task | None = None
        self._keep_alive_task: Task | None = None

    def start_ws(self):
        self._ws_task = asyncio.create_task(self.factorio_ws.start())
        self._keep_alive_task = asyncio.create_task(
            self.factorio_ws.keep_alive()
        )

    async def connect(self):
        logger.debug(f"FactorioZone connecting....")
        self.start_ws()
        await self.login()

    async def reconnect(self):
        logger.debug(f"FactorioZone reconnecting....")
        if self._ws_task:
            self._ws_task.cancel()
        if self._keep_alive_task:
            self._keep_alive_task.cancel()
        self.factorio_ws.clear_state()
        await self.connect()

    async def login(self) -> bool:
        while True:
            if not self.factorio_ws.visit_token:
                await asyncio.sleep(0.1)
                continue
            _data = {
                "userToken": self._token,
                "visitSecret": self.factorio_ws.visit_token.secret,
                "reconnected": "false",
                "script": urljoin(
                    CONFIG.factorio_zone.base_url,
                    "cache/main.c06a553abca88725685f.js",
                ),
                "revision": "3",
            }
            form = FormData()
            for item, value in _data.items():
                form.add_field(item, value)
            logger.debug(f"FactorioZone [Login] request_data={_data}")
            login_response = await self.session.post(
                url=urljoin(
                    CONFIG.factorio_zone.base_url,
                    "api/user/login",
                ),
                data=form,
            )
            logger.debug(f"FactorioZone [Login] status={login_response.status}")
            return login_response.ok

    async def status(self) -> StatusWS:
        return self.factorio_ws.status

    async def regions(self) -> Options:
        return self.factorio_ws.regions

    async def versions(self) -> Options:
        return self.factorio_ws.versions

    async def slots(self) -> Options:
        return self.factorio_ws.saves

    async def logs(self) -> list[Log]:
        return self.factorio_ws.logs

    async def start(
        self,
        region_id: str,
        version_id: str,
        slot_id: str,
    ) -> dict[bool, dict]:
        _data = {
            "visitSecret": self.factorio_ws.visit_token.secret,
            "region": region_id,
            "version": version_id,
            "save": slot_id,
            "ipv6": False,
            "options": None,
        }
        form = FormData()
        for item, value in _data.items():
            form.add_field(item, value)
        logger.debug(f"FactorioZone [StartServer] request_data={_data}")
        _response = await self.session.post(
            url=urljoin(
                CONFIG.factorio_zone.base_url,
                "api/instance/start",
            ),
            data=form,
        )
        logger.debug(
            f"FactorioZone [StartServer] {_response.status=}; "
            f"response={await _response.text()}"
        )
        return {_response.status == 200: await _response.json()}

    async def stop(self, launch_id: int):
        _data = {
            "visitSecret": self.factorio_ws.visit_token.secret,
            "launchId": launch_id,
        }
        form = FormData()
        for item, value in _data.items():
            form.add_field(item, value)
        logger.debug(f"FactorioZone [StopServer] request_data={_data}")
        _response = await self.session.post(
            url=urljoin(
                CONFIG.factorio_zone.base_url,
                "api/instance/stop",
            ),
            data=form,
        )
        logger.debug(
            f"FactorioZone [StopServer] {_response.status=}; "
            f"response={await _response.text()}"
        )
        return {_response.status == 200: await _response.json()}
