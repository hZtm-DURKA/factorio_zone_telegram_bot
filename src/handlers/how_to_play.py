from aiogram import Router
from aiogram.types import CallbackQuery

from filters import callback
from keyboards import keyboards

router: Router = Router()


TEXT = r"""
1) Загрузите / Выберите необходимую версию игры
2) <a href="https://github.com/hZtm-DURKA/factorio_mod_packs/releases">Загрузите моды</a> 
3) Закидываем в ...AppData\Roaming\Factorio\
4) Подключаемся...
"""


@router.callback_query(callback.HowPlay.filter())
async def how_to_play(callback_query: CallbackQuery):

    await callback_query.message.edit_text(
        text=TEXT,
        reply_markup=keyboards.back_to_main(),
    )
