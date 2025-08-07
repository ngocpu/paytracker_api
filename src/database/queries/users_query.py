class UserQueries:
    GET_USER_BY_ID = """
        SELECT * FROM users 
        WHERE user_id = %s AND is_deleted = FALSE
    """
    GET_USER_BY_EMAIL = """
        SELECT * FROM users WHERE email = %s AND is_deleted = FALSE
    """
    GET_USER_BY_NAME = """
        SELECT * FROM users WHERE username = %s AND is_deleted = FALSE
    """
    EMAIL_EXISTS = """
        SELECT COUNT(*) FROM users 
        WHERE email = %s AND is_deleted = FALSE
    """
    USERNAME_EXISTS = """
        SELECT COUNT(*) FROM users 
        WHERE username = %s AND is_deleted = FALSE
    """
    CREATE_USER = """
        INSERT INTO users (
            user_id, username, email, hashed_password, provider, 
            provider_id, preferred_language, role, is_active, is_deleted, created_at, updated_at, avatar
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    UPDATE_USER = """
        UPDATE Users SET 
            username = %s, email = %s, hashed_password = %s, 
            provider = %s, provider_id = %s, preferred_language = %s, 
            role = %s, is_active = %s, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = %s AND is_deleted = FALSE
    """

    # Status management queries
    ACTIVATE_USER = """
        UPDATE Users SET is_active = TRUE, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = %s
    """

    DEACTIVATE_USER = """
        UPDATE Users SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = %s
    """

    SOFT_DELETE_USER = """
        UPDATE Users SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = %s
    """

    UPDATE_LAST_LOGIN = """
        UPDATE Users SET updated_at = CURRENT_TIMESTAMP
        WHERE user_id = %s
    """

    # Delete and list queries
    HARD_DELETE_USER = """
        DELETE FROM Users WHERE user_id = %s
    """

    LIST_ALL_USERS = """
        SELECT * FROM Users WHERE is_deleted = FALSE
        ORDER BY created_at DESC
    """

    LIST_ACTIVE_USERS = """
        SELECT * FROM Users 
        WHERE is_deleted = FALSE AND is_active = TRUE
        ORDER BY created_at DESC
    """
    SAVE_VERIFICATION_CODE = """
        INSERT INTO otps(otp_id, user_id, otp_code, created_at, expires_at, is_used)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    VERIFY_CODE = """
        SELECT is_used FROM otps
WHERE user_id = %s AND otp_code = %s
ORDER BY created_at DESC LIMIT 1
    """
