CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    uuid CHAR(36) UNIQUE DEFAULT (UUID()), 
    email VARCHAR(255) UNIQUE NOT NULL, 
    password TEXT NOT NULL, 
    department_id INT(11) DEFAULT NULL, 
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



/*   For generating vpn configuration files*/
CREATE TABLE server_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ta_key TEXT NOT NULL,  -- TLS Auth Key
    ca_crt TEXT NOT NULL,  -- Certificate Authority Certificate
    server_crt TEXT NOT NULL,  -- Server Certificate
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE trusted_devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(255) UNIQUE NOT NULL,  -- Unique identifier for the device
    device_fingerprint VARCHAR(255) UNIQUE NOT NULL,  -- Fingerprint for device tracking
    device_name VARCHAR(255) NOT NULL, 
    device_type ENUM('desktop', 'laptop') NOT NULL, 
    device_os VARCHAR(255) NOT NULL,
    hardware_fingerprint VARCHAR(255) UNIQUE NOT NULL, -- Additional HW-based unique identifier
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

CREATE TABLE userDeviceMapping (
    id INT AUTO_INCREMENT PRIMARY KEY,
    u_id INT NOT NULL,
    d_id INT NOT NULL,  -- References `trusted_devices.device_id`
    status ENUM('active', 'revoked', 'pending') DEFAULT 'active',
    linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When the device was linked
    FOREIGN KEY (u_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (d_id) REFERENCES trusted_devices(id) ON DELETE CASCADE,
    UNIQUE (u_id, d_id) -- Ensures a user can't register the same device multiple times
);
