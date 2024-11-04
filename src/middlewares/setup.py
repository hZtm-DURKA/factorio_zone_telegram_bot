from aiogram import Dispatcher

from . import connection, auth_mw


def setup(dispatcher: Dispatcher):
    dispatcher.update.outer_middleware()(connection.db_connection_mw)
    dispatcher.update.outer_middleware()(auth_mw.auth_middleware)
