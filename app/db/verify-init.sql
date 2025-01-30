\c tx_manager;

-- List all tables
\dt

-- You can add more verification queries here
DO $$
BEGIN
    RAISE NOTICE 'Database initialization complete. Verifying tables...';
END $$;