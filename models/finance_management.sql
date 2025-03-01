CREATE TABLE category (
    category_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    transaction_type_id INT NOT NULL,
    category_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_type(transaction_type_id) ON DELETE CASCADE
);
CREATE TABLE transaction_type (
    transaction_type_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    type_name ENUM('Income', 'Expense') NOT NULL
);
CREATE TABLE transactions (
    transaction_id INT NOT NULL AUTO_INCREMENT,
    club_id INT NOT NULL,
    transaction_type_id INT NOT NULL,  -- 1 for Income, 2 for Expense
    category_id INT NULL,
    short_date DATE NOT NULL,
    transaction_description VARCHAR(100) NULL DEFAULT NULL,
    transaction_amount DECIMAL NOT NULL,
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (club_id) REFERENCES clubs(club_id),
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_types(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
