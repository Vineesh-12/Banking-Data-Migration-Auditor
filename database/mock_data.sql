USE BankingAuditDB;
GO

TRUNCATE TABLE dbo.MigratedAccounts;
GO

-- clean legacy data
INSERT INTO dbo.MigratedAccounts (AccountID, CustomerName, RoutingNumber, Balance, AccountType)
VALUES 
('ACC-1001', 'John Doe', '122105155', 1500.00, 'Checking'),
('ACC-1002', 'Jane Smith', '122105155', 45000.50, 'Savings'),
('ACC-1003', 'Robert Johnson', '122105155', 250.75, 'Checking'),
('ACC-1004', 'Emily Davis', '122105155', 12000.00, 'Savings'),
('ACC-1005', 'Michael Brown', '122105155', 850.00, 'Checking');

-- faulty data (simulating migration issues)
INSERT INTO dbo.MigratedAccounts (AccountID, CustomerName, RoutingNumber, Balance, AccountType)
VALUES 
('ACC-1006', 'William Wilson', '122105155', -50.00, 'Checking'),
('ACC-1007', 'Sarah Taylor', NULL, 3000.00, 'Savings'),
('ACC-1008', 'James Anderson', '', 500.00, 'Checking'),
('ACC-1001', 'John Doe Duplicate', '122105155', 1500.00, 'Checking'),
('ACC-1009', 'David Thomas', '122105155', 450.00, NULL),
('ACC-1010', 'Mary Jackson', '122105155', 999999999.99, 'Savings');
GO
