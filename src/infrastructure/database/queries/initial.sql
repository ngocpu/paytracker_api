CREATE TABLE Users (
    user_id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    provider VARCHAR(50),
    provider_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    preferred_language ENUM('vi', 'en') DEFAULT 'vi',
    role ENUM('user', 'admin') DEFAULT 'user',
    is_active BOOLEAN DEFAULT FALSE,
    is_deleted BOOLEAN DEFAULT FALSE,
    INDEX idx_users_email_provider (email, provider_id)
);
CREATE TABLE Refreshtoken (
    token_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    refresh_token VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Cateegory table
CREATE TABLE Categories (
    category_id VARCHAR(36) PRIMARY KEY,
    name_en VARCHAR(100) NOT NULL,
    name_vi VARCHAR(100) NOT NULL,
    icon_url VARCHAR(512),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
-- Tránsaction table
CREATE TABLE Transactions (
    transaction_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    amount DECIMAL(15,2),
    category_id VARCHAR(36),
    note TEXT,
    date DATETIME,
    source ENUM('text', 'voice'),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    INDEX idx_transactions_user_date (user_id, date)
);

-- Budgets
CREATE TABLE Budgets (
    budget_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    month CHAR(7),
    total_income DECIMAL(15,2),
    jar_essential DECIMAL(15,2),
    jar_saving DECIMAL(15,2),
    jar_education DECIMAL(15,2),
    jar_enjoyment DECIMAL(15,2),
    jar_giving DECIMAL(15,2),
    jar_investment DECIMAL(15,2),
    spent_essential DECIMAL(15,2),
    spent_saving DECIMAL(15,2),
    spent_education DECIMAL(15,2),
    spent_enjoyment DECIMAL(15,2),
    spent_giving DECIMAL(15,2),
    spent_investment DECIMAL(15,2),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    INDEX idx_budgets_user_month (user_id, month)
);

-- Goals
CREATE TABLE Goals (
    goal_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    name VARCHAR(100),
    target_amount DECIMAL(15,2),
    current_amount DECIMAL(15,2),
    deadline DATE,
    status ENUM('active', 'completed', 'failed'),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    INDEX idx_goals_user (user_id)
);

-- Notifications
CREATE TABLE Notifications (
    notification_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    type ENUM('budget_alert', 'goal_reminder', 'report', 'system'),
    title VARCHAR(100),
    message TEXT,
    channel ENUM('push'),
    status ENUM('pending', 'sent', 'failed'),
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME,
    sent_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    INDEX idx_notifications_user_created_isread (user_id, created_at, is_read)
);

-- SystemLogs
CREATE TABLE SystemLogs (
    log_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    action VARCHAR(100),
    details TEXT,
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    INDEX idx_systemlogs_user_created (user_id, created_at)
);

