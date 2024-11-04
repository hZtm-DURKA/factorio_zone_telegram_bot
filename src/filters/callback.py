from aiogram.filters.callback_data import CallbackData


class MainMenu(CallbackData, prefix="main_menu"):
    pass


class HowPlay(CallbackData, prefix="how_play"):
    pass


class StatusServer(CallbackData, prefix="status_server"):
    pass


class StopServer(CallbackData, prefix="stop_server"):
    launch_id: int


class LogsServer(CallbackData, prefix="logs_server"):
    pass


class PreparingStart(CallbackData, prefix="preparing_server"):
    pass


class SelectRegion(CallbackData, prefix="select_region"):
    region_id: str


class SelectVersion(CallbackData, prefix="select_version"):
    region_id: str
    version_id: str


class SelectSave(CallbackData, prefix="select_save"):
    region_id: str
    version_id: str
    slot_id: str


class StartServer(CallbackData, prefix="start_server"):
    region_id: str
    version_id: str
    slot_id: str
