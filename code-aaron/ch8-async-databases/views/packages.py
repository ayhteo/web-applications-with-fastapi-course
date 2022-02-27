import fastapi
from fastapi import Request
from fastapi.templating import Jinja2Templates
from view_models.packages.details_viewmodel import DetailsViewModel

router = fastapi.APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/project/{package_name}", include_in_schema=False)
async def details(package_name: str, request: Request):
    vm = DetailsViewModel(request, package_name=package_name)
    await vm.load()
    return templates.TemplateResponse("packages/details.html", vm.to_dict())
