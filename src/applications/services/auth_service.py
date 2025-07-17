import uuid
from datetime import datetime, timedelta
from src.applications.utils.hash_password import PasswordUtils
from src.applications.utils.validation import VerificationUtlils
from src.applications.utils.jwt import JWTUtils
from src.domains.entities.users import User, PreferredLanguage, UserRole
from src.infrastructure.repository.users_repo_impl import UsersRepoImpl
from src.applications.DTOs.auth_dto import (
    RegisterRequest,
    LoginRequest,
    AuthResponse,
    RegisterResponse,
    UserResponse,
)
from src.infrastructure.services.mail_service import SMTPEmailService
from src.infrastructure.services.oauth_service import GoogleOAuthService


class AuthService:
    def __init__(
        self,
        users_repo: UsersRepoImpl,
        mail_service: SMTPEmailService,
        google_service: GoogleOAuthService,
    ):
        self.users_repo = users_repo
        self.mail_service = mail_service
        self.google_service = google_service

    def register_user(self, req: RegisterRequest) -> RegisterResponse:
        try:
            if self.users_repo.email_exists(req.email):
                raise ValueError("Email already exists")
            if self.users_repo.username_exists(req.username):
                raise ValueError("Username already exists")
            hashed_password = PasswordUtils.hash_password(req.password)

            user = User(
                user_id=str(uuid.uuid4()),
                email=req.email,
                username=req.username,
                hashed_password=hashed_password,
                preferred_language=PreferredLanguage(req.preferred_language),
                provider=None,
                provider_id=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                role=UserRole.USER,
                is_active=False,
                is_deleted=False,
            )
            created_user = self.users_repo.create_user(user)
            if not created_user:
                raise ValueError("Failed to create user")
            verification_code = VerificationUtlils.generate_verification_code()

            self.users_repo.save_verification_code(
                str(uuid.uuid4()),
                created_user.user_id,
                verification_code,
                datetime.utcnow(),
                datetime.utcnow() + timedelta(minutes=5),
                False,
            )
            subject = "Email Verification"
            body = f"Your verification code is: {verification_code}"
            self.mail_service.send_email(
                to=created_user.email, subject=subject, body=body
            )
            return RegisterResponse(
                message="User registered successfully. Please check your email for verification code.",
                user_id=created_user.user_id,
                email=created_user.email,
            )
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Registration failed: {str(e)}")

    def activate_account(self, user_id: str, code: str) -> AuthResponse:
        try:
            if not self.users_repo.verify_code(user_id, code):
                raise ValueError("Invalid verification code")
            self.users_repo.activate_user(user_id)
            user = self.users_repo.get_user_by_id(user_id)
            user_response = UserResponse(
                user_id=user.user_id,
                username=user.username,
                email=user.email,
                preferred_language=(
                    user.preferred_language.value
                    if hasattr(user.preferred_language, "value")
                    else user.preferred_language
                ),
                role=user.role.value if hasattr(user.role, "value") else user.role,
                is_active=user.is_active,
                avatar_url=user.avatar,
                provider=user.provider,
                provider_id=user.provider_id,
            )
            access_tokens = JWTUtils.generate_access_token(
                user_id, email=user.email, role=user.role
            )
            refresh_tokens = JWTUtils.generate_refresh_token(
                user_id, email=user.email, role=user.role
            )
            return AuthResponse(
                user=user_response,
                access_tokens=access_tokens,
                refresh_tokens=refresh_tokens,
                message="Account activated successfully.",
            )
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Account activation failed: {str(e)}")

    def login_user(self, req: LoginRequest) -> AuthResponse:
        try:
            user = self.users_repo.get_user_by_email(req.email)
            if not user or not PasswordUtils.check_password(
                req.password, user.hashed_password
            ):
                raise ValueError("Invalid email or password")
            if not user.is_active:
                raise ValueError("Account is not active. Please activate your account.")
            access_tokens = JWTUtils.generate_access_token(
                user.user_id, email=user.email, role=user.role
            )
            refresh_tokens = JWTUtils.generate_refresh_token(
                user.user_id, email=user.email, role=user.role
            )
            self.users_repo.update_last_login(user.user_id)
            return AuthResponse(
                user=user,
                access_tokens=access_tokens,
                refresh_tokens=refresh_tokens,
                message="Login successful.",
            )
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}")

    def refresh_tokens(self, user_id: str) -> AuthResponse:
        try:
            user = self.users_repo.get_user_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            access_tokens = JWTUtils.generate_access_token(
                user_id, email=user.email, role=user.role
            )
            refresh_tokens = JWTUtils.generate_refresh_token(
                user_id, email=user.email, role=user.role
            )
            return AuthResponse(
                user=user,
                access_tokens=access_tokens,
                refresh_tokens=refresh_tokens,
                message="Tokens refreshed successfully.",
            )
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Token refresh failed: {str(e)}")

    def logout_user(self, user_id: str) -> dict:
        try:
            user = self.users_repo.get_user_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            # Invalidate tokens logic can be added here
            return {"message": "Logout successful."}
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Logout failed: {str(e)}")

    def google_login(self, code: str) -> AuthResponse:
        try:
            user_info = self.google_service.get_user_info(code)
            email = user_info.get("email")
            if not email:
                raise ValueError("Email not found in Google user info")
            user = self.users_repo.get_user_by_email(email)
            if not user:
                user = User(
                    user_id=str(uuid.uuid4()),
                    email=email,
                    username=user_info.get("name", "GoogleUser"),
                    avatar=user_info.get("picture"),
                    hashed_password=None,  # No password for OAuth users
                    preferred_language=PreferredLanguage.EN,
                    provider="google",
                    provider_id=user_info.get("sub"),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    role=UserRole.USER,
                    is_active=True,
                    is_deleted=False,
                )
                self.users_repo.create_user(user)
            access_tokens = JWTUtils.generate_access_token(
                user.user_id, email=user.email, role=user.role
            )
            refresh_tokens = JWTUtils.generate_refresh_token(
                user.user_id, email=user.email, role=user.role
            )
            return AuthResponse(
                user=user,
                access_tokens=access_tokens,
                refresh_tokens=refresh_tokens,
                message="Google login successful.",
            )
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Google login failed: {str(e)}")
