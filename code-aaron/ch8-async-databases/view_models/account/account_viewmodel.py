from view_models.shared.viewmodel import ViewModelBase
from data.user import User
from fastapi import Request
import services.user_service as user_service
from typing import Optional


class AccountViewModel(ViewModelBase):
    def __init__(
        self,
        request: Request,
    ):
        super().__init__(request)
        self.user: Optional[User] = None

    async def load(self):
        self.user = await user_service.get_user_by_id(self.user_id)
