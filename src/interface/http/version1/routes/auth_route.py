from fastapi import APIRouter, Body, HTTPException
from src.applications.DTOs.auth_dto import RegisterRequest, LoginRequest
from src.interface.http.common.container import auth_controller


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register_user(req: RegisterRequest = Body(...)):
    res = auth_controller.register_user(req)
    if hasattr(res, "status_code") and res.status_code != 201:
        raise HTTPException(status_code=res.status_code, detail=res.message)
    return res

@router.post("/activate")
def activate_account(user_id: str = Body(...), code: str = Body(...)):
    res = auth_controller.activate_account(user_id, code)
    if hasattr(res, "status_code") and res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=res.message)
    return res

@router.post("/login")
def login_user(req: LoginRequest = Body(...)):
    res = auth_controller.login_user(req)
    if hasattr(res, "status_code") and res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=res.message)
    return res

@router.post("/google-login")
def google_login(code: str = Body(...)):
    res = auth_controller.google_login(code)
    if hasattr(res, "status_code") and res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=res.message)
    return res