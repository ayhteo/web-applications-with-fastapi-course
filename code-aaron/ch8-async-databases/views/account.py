import fastapi
from fastapi import Request
from view_models.account.account_viewmodel import AccountViewModel
from view_models.account.login_viewmodel import LoginViewModel
from view_models.account.register_viewmodel import RegisterViewModel
from fastapi.templating import Jinja2Templates
from services import user_service
from starlette import status
from infrastructure import cookie_auth
import asyncio

router = fastapi.APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/account", include_in_schema=False)
async def account(request: Request, user: str = "guest"):
    vm = AccountViewModel(request)
    await vm.load()
    return templates.TemplateResponse("/account/index.html", vm.to_dict())


@router.get("/account/register", include_in_schema=False)
async def register(request: Request):
    vm = RegisterViewModel(request)
    return templates.TemplateResponse("/account/register.html", vm.to_dict())


@router.post("/account/register", include_in_schema=False)
async def register(request: Request):
    print("POST REGISTER")
    vm = RegisterViewModel(request)
    await vm.load()
    if vm.error:
        print(vm.error)
        return templates.TemplateResponse("/account/register.html", vm.to_dict())
    account = await user_service.create_account(vm.name, vm.email, vm.password)
    # login user
    response = fastapi.responses.RedirectResponse(
        url="/account", status_code=status.HTTP_302_FOUND
    )
    cookie_auth.set_auth(response=response, user_id=account.id)
    return response


@router.get("/account/login", include_in_schema=False)
async def login_get(request: Request):
    vm = LoginViewModel(request)
    return templates.TemplateResponse("/account/login.html", vm.to_dict())


@router.post("/account/login", include_in_schema=False)
async def login_post(request: Request):
    vm = LoginViewModel(request)
    await vm.load()
    if vm.error:
        return templates.TemplateResponse("/account/login.html", vm.to_dict())
    user = await user_service.login_user(vm.email, vm.password)
    if not user:
        await asyncio.sleep(5)
        vm.error = "That account does not exist or the password is incorrect."
        return templates.TemplateResponse("/account/login.html", vm.to_dict())
    resp = fastapi.responses.RedirectResponse(
        "/account", status_code=status.HTTP_302_FOUND
    )
    cookie_auth.set_auth(resp, user.id)
    return resp


@router.get("/account/logout", include_in_schema=False)
def logout():
    response = fastapi.responses.RedirectResponse(
        url="/", status_code=status.HTTP_302_FOUND
    )
    cookie_auth.logout(response=response)
    return response