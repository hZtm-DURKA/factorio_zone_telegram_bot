from enum import Enum

from attr import dataclass
from pydantic import BaseModel


class Log(BaseModel):
    launchId: int | None = None
    line: str = ""
    time: int | None = None
    num: int | None = None
    type: str = ""


class Slot(BaseModel):
    region: str | None = ""
    slot: str | None = ""
    version: str | None = ""


class StatusEnum(Enum):
    stopping = "stopping"
    starting = "starting"
    running = "running"


class StatusServer(BaseModel):
    launchId: int | None = None
    type: StatusEnum = StatusEnum.stopping
    socket: str | None = ""


@dataclass
class StatusWS:
    running_ws: bool
    server: StatusServer
    slot: Slot | None = None


class SecretVisit(BaseModel):
    secret: str
    type: str


class Options(BaseModel):
    options: dict[str, str]
