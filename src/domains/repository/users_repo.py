from abc import ABC, abstractmethod
from typing import Optional, List
from src.domains.entities.users import User

class UsersRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        pass

    # @abstractmethod
    # def get_user_by_provider_id(self, provider: str, provider_id: str) -> Optional[User]:
    #     pass

    @abstractmethod
    def email_exists(self, email: str) -> bool:
        pass

    @abstractmethod
    def username_exists(self, username: str) -> bool:
        pass

    @abstractmethod
    def activate_user(self, user_id: str) -> None:
        pass

    @abstractmethod
    def deactivate_user(self, user_id: str) -> None:
        pass

    @abstractmethod
    def update_last_login(self, user_id: str) -> None:
        pass

    @abstractmethod
    def soft_delete_user(self, user_id: str) -> None:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        pass

    @abstractmethod
    def list_users(self) -> List[User]:
        pass
    @abstractmethod
    def save_verification_code(self, user_id: str, code: str) -> None:
        pass
    @abstractmethod
    def verify_code(self, user_id: str, code: str) -> bool:
        pass