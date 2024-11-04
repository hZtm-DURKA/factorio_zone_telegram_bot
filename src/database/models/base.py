from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True

    # @property
    # def __tablename__(self):
    #     return re.sub(
    #         r"(?<!^)(?=[A-Z])",
    #         "_",
    #         self.__class__.__name__,
    #     ).lower()
