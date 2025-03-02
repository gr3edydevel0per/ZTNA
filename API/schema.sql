CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    uuid CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL, -- Store hashed passwords
    department_id INT, -- Links user to a department
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
);


CREATE TABLE certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uuid CHAR(36) NOT NULL,
    certificate TEXT NOT NULL, -- Stores the actual certificate
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL, -- Expiry date of the certificate
    status ENUM('active', 'revoked', 'expired') DEFAULT 'active',
    FOREIGN KEY (uuid) REFERENCES users(uuid) ON DELETE CASCADE
);

CREATE TABLE cert_gen_re (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uuid CHAR(36) NOT NULL,
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'approved', 'rejected', 'completed') DEFAULT 'pending',
    cert_action ENUM('generation', 'revocation') DEFAULT 'generation',
    csr TEXT, -- Stores the certificate signing request for generation
    FOREIGN KEY (uuid) REFERENCES users(uuid) ON DELETE CASCADE
);


CREATE TABLE server_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ta_key TEXT NOT NULL,  -- TLS Auth Key
    ca_crt TEXT NOT NULL,  -- Certificate Authority Certificate
    server_crt TEXT NOT NULL,  -- Server Certificate
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
