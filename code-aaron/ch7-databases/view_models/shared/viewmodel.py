from typing import Optional
from fastapi.requests import Request
from infrastructure import cookie_auth


class ViewModelBase:
    def __init__(self, request: Request):
        self.request: Request = request
        self.error: Optional[str] = None
        self.user_id: Optional[int] = cookie_auth.get_user_id_from_auth_cookie(request)
        self.is_logged_in = self.user_id if self.user_id is not None else None

    def to_dict(self) -> dict:
        return self.__dict__
