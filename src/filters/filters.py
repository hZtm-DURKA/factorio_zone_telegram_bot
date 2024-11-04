from aiogram.filters import Command, Filter


start_command = Command("factorio")
registration_command = Command("registration")


class TokenFilter(Filter):
    def __init__(self, token: str):
        self.token = token

    async def __call__(self, *args, **kwargs):
        if command := kwargs.get("command"):
            return command.args == self.token
        return False


class OnlyActiveUserFilter(Filter):

    async def __call__(self, *args, **kwargs):
        if user := kwargs.get("user"):
            return user.active == True
        return False
