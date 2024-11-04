from aiogram import Router
from aiogram.types import CallbackQuery

from filters import callback
from keyboards import keyboards

router: Router = Router()


TEXT = r"""
1) Качаем Factorio v1.1.110
2) <a href="https://github.com/HzTeam-DURKA/factorio/releases/tag/v0.1.0">Качаем моды</a> 
3) Закидываем в ...AppData\Roaming\Factorio\mods
4) Подключаемся...
"""


@router.callback_query(callback.HowPlay.filter())
async def how_play(callback_query: CallbackQuery):

    await callback_query.message.edit_text(
        text=TEXT,
        reply_markup=keyboards.back_to_main(),
    )
