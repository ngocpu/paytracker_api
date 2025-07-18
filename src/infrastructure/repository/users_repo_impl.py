from typing import Optional, List, Tuple, Any
from src.infrastructure.database.connection import get_database_connection
from src.domains.repository.users_repo import UsersRepository
from src.domains.entities.users import User, PreferredLanguage, UserRole
from src.infrastructure.database.queries.user_query import UserQueries
from datetime import datetime

class UsersRepoImpl(UsersRepository):

    def _execute_query(
        self,
        query: str,
        params: Tuple = (),
        fetch_one: bool = False,
        fetch_all: bool = False,
        commit: bool = False,
    ) -> Any:
        """
        Base method để execute query với error handling
        """
        conn = get_database_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)

            if commit:
                conn.commit()
                return True
            elif fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                return cursor.fetchone()

        except Exception as e:
            print(f"Database error: {e}")
            if commit and conn:
                conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _execute_count_query(self, query: str, params: Tuple = ()) -> bool:
        """
        Base method cho các query count (kiểm tra tồn tại)
        """
        conn = get_database_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result[0] > 0 if result else False
        except Exception as e:
            print(f"Database error: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def map_to_entity(self, row: dict) -> Optional[User]:
        """Convert database row to User entity"""
        if not row:
            return None

        return User(
            user_id=row["user_id"],
            username=row["username"],
            email=row["email"],
            hashed_password=row["hashed_password"],
            provider=row["provider"],
            provider_id=row["provider_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            preferred_language=PreferredLanguage(row["preferred_language"]),
            role=UserRole(row["role"]),
            is_active=row["is_active"],
            is_deleted=row["is_deleted"],
        )

    # Bây giờ các method chỉ cần 1 dòng!
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        result = self._execute_query(
            UserQueries.GET_USER_BY_ID, (user_id,), fetch_one=True
        )
        return self.map_to_entity(result) if result else None

    def get_user_by_email(self, email: str) -> Optional[User]:
        result = self._execute_query(
            UserQueries.GET_USER_BY_EMAIL, (email,), fetch_one=True
        )
        return self.map_to_entity(result) if result else None

    def get_user_by_username(self, username: str) -> Optional[User]:
        result = self._execute_query(
            UserQueries.GET_USER_BY_USERNAME, (username,), fetch_one=True
        )
        return self.map_to_entity(result) if result else None

    def get_user_by_provider_id(
        self, provider: str, provider_id: str
    ) -> Optional[User]:
        result = self._execute_query(
            UserQueries.GET_USER_BY_PROVIDER_ID, (provider, provider_id), fetch_one=True
        )
        return self.map_to_entity(result) if result else None

    def email_exists(self, email: str) -> bool:
        return self._execute_count_query(UserQueries.EMAIL_EXISTS, (email,))

    def username_exists(self, username: str) -> bool:
        return self._execute_count_query(UserQueries.USERNAME_EXISTS, (username,))

    def create_user(self, user: User) -> User:
        success = self._execute_query(
            UserQueries.CREATE_USER,
            (
                user.user_id,
                user.username,
                user.email,
                user.hashed_password,
                user.provider,
                user.provider_id,
                user.preferred_language.value,
                user.role.value,
                user.is_active,
                user.is_deleted,
                user.created_at,
                user.updated_at,
                user.avatar,
            ),
            commit=True,
        )
        print(f"Create user success: {success}")
        return user if success else None

    def update_user(self, user: User) -> User:
        success = self._execute_query(
            UserQueries.UPDATE_USER,
            (
                user.username,
                user.email,
                user.hashed_password,
                user.provider,
                user.provider_id,
                user.preferred_language.value,
                user.role.value,
                user.is_active,
                user.user_id,
            ),
            commit=True,
        )
        return user if success else None

    def save_verification_code(self, otp_id: str, user_id: str, code: str, created_at: datetime, expires_at: datetime, is_used: bool = False) -> any:
        self._execute_query(
            UserQueries.SAVE_VERIFICATION_CODE, (otp_id, user_id, code, created_at, expires_at, is_used), commit=True
        )

    def verify_code(self, user_id: str, code: str) -> bool:
        result = self._execute_query(
            UserQueries.VERIFY_CODE, (user_id, code), fetch_one=True
        )
        return result is not None and not result["is_used"]

    def activate_user(self, user_id: str) -> None:
        self._execute_query(UserQueries.ACTIVATE_USER, (user_id,), commit=True)

    def deactivate_user(self, user_id: str) -> None:
        self._execute_query(UserQueries.DEACTIVATE_USER, (user_id,), commit=True)

    def soft_delete_user(self, user_id: str) -> None:
        self._execute_query(UserQueries.SOFT_DELETE_USER, (user_id,), commit=True)

    def delete_user(self, user_id: str) -> None:
        self._execute_query(UserQueries.HARD_DELETE_USER, (user_id,), commit=True)

    def update_last_login(self, user_id: str) -> None:
        self._execute_query(UserQueries.UPDATE_LAST_LOGIN, (user_id,), commit=True)

    def list_users(self) -> List[User]:
        results = self._execute_query(UserQueries.LIST_ALL_USERS, fetch_all=True)
        return [self.map_to_entity(row) for row in results] if results else []
