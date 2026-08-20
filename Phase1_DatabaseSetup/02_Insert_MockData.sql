-- =======================================================
-- Phase 1: Insert Mock Data (Intentionally Corrupted)
-- =======================================================

USE BankingAuditDB;
GO

-- Clear out any existing data if re-running
TRUNCATE TABLE dbo.MigratedAccounts;
GO

-- Insert Clean Data (Expected correct format)
INSERT INTO dbo.MigratedAccounts (AccountID, CustomerName, RoutingNumber, Balance, AccountType)
VALUES 
('ACC-1001', 'John Doe', '122105155', 1500.00, 'Checking'),
('ACC-1002', 'Jane Smith', '122105155', 45000.50, 'Savings'),
('ACC-1003', 'Robert Johnson', '122105155', 250.75, 'Checking'),
('ACC-1004', 'Emily Davis', '122105155', 12000.00, 'Savings'),
('ACC-1005', 'Michael Brown', '122105155', 850.00, 'Checking');

-- Insert Corrupted Data (Simulating Migration Errors)
INSERT INTO dbo.MigratedAccounts (AccountID, CustomerName, RoutingNumber, Balance, AccountType)
VALUES 
-- ERROR 1: Negative Balance (Should not be possible for standard accounts)
('ACC-1006', 'William Wilson', '122105155', -50.00, 'Checking'),

-- ERROR 2: Missing Routing Number (NULL)
('ACC-1007', 'Sarah Taylor', NULL, 3000.00, 'Savings'),

-- ERROR 3: Blank/Empty Routing Number
('ACC-1008', 'James Anderson', '', 500.00, 'Checking'),

-- ERROR 4: Duplicate Account ID (We will insert a duplicate in the next step to simulate this error if no primary key on AccountID)
('ACC-1001', 'John Doe Duplicate', '122105155', 1500.00, 'Checking'),

-- ERROR 5: Missing Account Type (NULL)
('ACC-1009', 'David Thomas', '122105155', 450.00, NULL),

-- ERROR 6: Extremely High Unrealistic Balance (Data type issue from legacy system)
('ACC-1010', 'Mary Jackson', '122105155', 999999999.99, 'Savings');

GO

-- Verify the inserted data
SELECT * FROM dbo.MigratedAccounts;
GO
