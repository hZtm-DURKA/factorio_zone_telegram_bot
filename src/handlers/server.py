import re

from aiogram import Router
from aiogram.types import CallbackQuery

from filters import callback
from filters import filters
from keyboards import keyboards
from misc.factorio_zone import FactorioZone

router: Router = Router()


@router.callback_query(
    callback.StopServer.filter(),
    filters.OnlyActiveUserFilter(),
)
async def shutdown(
    callback_query: CallbackQuery,
    callback_data: callback.StopServer,
    factorio_zone: FactorioZone,
):
    await callback_query.message.edit_text(
        text="Выключается....",
        reply_markup=keyboards.back_to_main(),
    )
    status = await factorio_zone.stop(launch_id=callback_data.launch_id)
    if response := status.get(False):
        response_message = response.get("responseMessage")
        await callback_query.message.edit_text(
            text=f"Хуйню ты что-то натыкал: \n\n<code>{response_message}</code>",
            reply_markup=keyboards.back_to_main(),
        )


@router.callback_query(
    callback.PreparingStart.filter(),
)
async def preparing(
    callback_query: CallbackQuery,
    factorio_zone: FactorioZone,
):
    await callback_query.message.edit_text(
        text="Выберите регион:",
        reply_markup=keyboards.show_region(
            options=await factorio_zone.regions()
        ),
    )


@router.callback_query(
    callback.SelectRegion.filter(),
)
async def select_version(
    callback_query: CallbackQuery,
    factorio_zone: FactorioZone,
    callback_data: callback.SelectRegion,
):
    regions = await factorio_zone.regions()
    text = (
        f"Регион: {regions.options[callback_data.region_id]}\n"
        f"Выберите версию:"
    )
    await callback_query.message.edit_text(
        text=text,
        reply_markup=keyboards.show_versions(
            region_id=callback_data.region_id,
            options=await factorio_zone.versions(),
        ),
    )


@router.callback_query(
    callback.SelectVersion.filter(),
)
async def select_slots(
    callback_query: CallbackQuery,
    factorio_zone: FactorioZone,
    callback_data: callback.SelectVersion,
):
    regions = await factorio_zone.regions()
    versions = await factorio_zone.versions()
    text = (
        f"Регион: {regions.options[callback_data.region_id]} \n"
        f"Версия: {versions.options[callback_data.version_id]} \n"
        f"Выберите сохранение:"
    )
    await callback_query.message.edit_text(
        text=text,
        reply_markup=keyboards.show_slots(
            region_id=callback_data.region_id,
            version_id=callback_data.version_id,
            options=await factorio_zone.slots(),
        ),
    )


@router.callback_query(
    callback.SelectSave.filter(),
)
async def completed_start(
    callback_query: CallbackQuery,
    factorio_zone: FactorioZone,
    callback_data: callback.SelectSave,
):
    regions = await factorio_zone.regions()
    versions = await factorio_zone.versions()
    slots = await factorio_zone.slots()
    text = (
        f"Регион: {regions.options[callback_data.region_id]} \n"
        f"Версия: {versions.options[callback_data.version_id]} \n"
        f"Сохранение: {slots.options[callback_data.slot_id]} \n\n"
        f"Жми на рычаг Кронк!"
    )
    await callback_query.message.edit_text(
        text=text,
        reply_markup=keyboards.complete_start(
            region_id=callback_data.region_id,
            version_id=callback_data.version_id,
            slot_id=callback_data.slot_id,
        ),
    )


@router.callback_query(
    callback.StartServer.filter(),
)
async def start_server(
    callback_query: CallbackQuery,
    factorio_zone: FactorioZone,
    callback_data: callback.StartServer,
):
    await callback_query.message.edit_text(text="Запускается....")
    status = await factorio_zone.start(
        region_id=callback_data.region_id,
        version_id=callback_data.version_id,
        slot_id=callback_data.slot_id,
    )
    if response := status.get(False):
        response_message = response.get("responseMessage")
        await callback_query.message.edit_text(
            text=f"Хуйню ты что-то натыкал: \n\n<code>{response_message}</code>",
            reply_markup=keyboards.back_to_main(),
        )


@router.callback_query(
    callback.LogsServer.filter(),
)
async def show_logs(
    callback_query: CallbackQuery,
    factorio_zone: FactorioZone,
):
    logs = await factorio_zone.logs()
    text_log = "\n".join([log.line.strip() for log in logs[-5:]])
    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}(?::\d{1,5})?\b"
    replacement = "'ip hidden ;)'"
    await callback_query.message.edit_text(
        text=re.sub(ip_pattern, replacement, text_log),
        reply_markup=keyboards.back_to_main(),
    )
