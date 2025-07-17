from src.applications.services.auth_service import AuthService
from src.infrastructure.services.mail_service import SMTPEmailService
from src.infrastructure.services.oauth_service import GoogleOAuthService
from src.infrastructure.repository.users_repo_impl import UsersRepoImpl
from src.interface.http.version1.controller.auth_controler import AuthController

user_repo = UsersRepoImpl()
mail_service = SMTPEmailService()
google_service = GoogleOAuthService()
auth_service = AuthService(user_repo, mail_service, google_service)
auth_controller = AuthController(auth_service)
