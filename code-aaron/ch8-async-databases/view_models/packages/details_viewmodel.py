from click import Option
from view_models.shared.viewmodel import ViewModelBase
from fastapi import Request
from services import package_service
from data.release import Release
from data.package import Package
import datetime
from typing import Optional


class DetailsViewModel(ViewModelBase):
    def __init__(self, request: Request, package_name: str):
        super().__init__(request)
        self.package_name = package_name
        self.is_latest = True
        self.package: Optional[Package] = None
        self.latest_release: Optional[Release] = None
        self.maintainers = []

    async def load(self):
        self.package = await package_service.get_package_by_id(self.package_name)
        self.latest_release = await package_service.get_latest_release_for_package(
            self.package_name
        )
        if not self.package or not self.latest_release:
            return
        r = self.latest_release
        self.latest_version = f"{r.major_ver}.{r.minor_ver}.{r.build_ver}"
