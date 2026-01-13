CREATE TABLE IF NOT EXISTS schools (
    affiliation_number VARCHAR(255) PRIMARY KEY,
    school_name VARCHAR(255),
    address TEXT,
    city VARCHAR(100),
    district VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(20),
    phone VARCHAR(50),
    email VARCHAR(255),
    website VARCHAR(255),
    source VARCHAR(50) DEFAULT 'saras',
    last_scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email_confidence VARCHAR(20) DEFAULT 'HIGH'
);
