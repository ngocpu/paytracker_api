from src.applications.services.auth_service import AuthService
from src.applications.DTOs.auth_dto import RegisterRequest, LoginRequest
from src.interface.http.common.response import HttpErrorResponse , HttpResponse
class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def register_user(self, req:RegisterRequest) -> dict:
        try:
            res = self.auth_service.register_user(req)
            return HttpResponse(
                status_code=201,
                message="User registered successfully.",
                data=res
            )
        except Exception as e:
            return HttpErrorResponse(
                status_code=400,
                message=str(e),
                error_code="REGISTRATION_ERROR"
            )

    def activate_account(self, user_id:str, code:str) -> dict:
        try:
            res = self.auth_service.activate_account(user_id, code)
            return HttpResponse(
                status_code=200,
                message="Account activated successfully.",
                data=res
            )
        except Exception as e:
            return HttpErrorResponse(
                status_code=400,
                message=str(e),
                error_code="ACTIVATION_ERROR"
            )
    def login_user(self, req:LoginRequest) -> dict:
        try:
            res = self.auth_service.login_user(req)
            return HttpResponse(
                status_code=200,
                message="User logged in successfully.",
                data=res
            )
        except Exception as e:
            return HttpErrorResponse(
                status_code=400,
                message=str(e),
                error_code="LOGIN_ERROR"
            )
    def google_login(self, code: str) -> dict:
        try:
            res = self.auth_service.google_login(code)
            return HttpResponse(
                status_code=200,
                message="User logged in successfully via Google.",
                data=res
            )
        except Exception as e:
            return HttpErrorResponse(
                status_code=400,
                message=str(e),
                error_code="GOOGLE_LOGIN_ERROR"
            )
    def refresh_tokens(self, user_id: str) -> dict:
        try:
            res = self.auth_service.refresh_tokens(user_id)
            return HttpResponse(
                status_code=200,
                message="Tokens refreshed successfully.",
                data=res
            )
        except Exception as e:
            return HttpErrorResponse(
                status_code=400,
                message=str(e),
                error_code="TOKEN_REFRESH_ERROR"
            )

    def logout_user(self, user_id: str) -> dict:
        try:
            res = self.auth_service.logout_user(user_id)
            return HttpResponse(
                status_code=200,
                message="User logged out successfully.",
                data=res
            )
        except Exception as e:
            return HttpErrorResponse(
                status_code=400,
                message=str(e),
                error_code="LOGOUT_ERROR"
            )
    