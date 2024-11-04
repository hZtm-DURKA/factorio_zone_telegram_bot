from sqlalchemy.orm import Session


class BaseQuery:

    def __init__(self, session: Session):
        self._session = session
