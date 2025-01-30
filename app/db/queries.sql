-- First, connect to the database
\c tx_manager

-- Add error handling wrapper
DO $$
BEGIN
    RAISE NOTICE 'Starting table creation...';

    -- Create the accounts table if it doesn't exist
    CREATE TABLE IF NOT EXISTS accounts (
        id BIGSERIAL PRIMARY KEY,
        account_name VARCHAR(255) NOT NULL UNIQUE,
        account_number VARCHAR(50) UNIQUE,
        balance DECIMAL(10, 2) DEFAULT 0.00,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create the transactions table if it doesn't exist
    CREATE TABLE IF NOT EXISTS transactions (
        id BIGSERIAL PRIMARY KEY,
        transaction_date TIMESTAMP NOT NULL,
        from_account BIGINT REFERENCES accounts(id) ON DELETE RESTRICT,
        to_account BIGINT REFERENCES accounts(id) ON DELETE RESTRICT,
        transaction_amount DECIMAL(10,2) NOT NULL CHECK (transaction_amount > 0),
        remarks VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    RAISE NOTICE 'Tables created successfully';
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Error creating tables: %', SQLERRM;
    RAISE;
END
$$;

-- Verify the tables were created
\dt accounts
\dt transactions