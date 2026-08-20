-- Ensure database exists
IF NOT EXISTS (SELECT name FROM master.dbo.sysdatabases WHERE name = N'BankingAuditDB')
BEGIN
    CREATE DATABASE BankingAuditDB;
END
GO

USE BankingAuditDB;
GO

-- Recreate target migration table
IF OBJECT_ID('dbo.MigratedAccounts', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.MigratedAccounts;
END
GO

CREATE TABLE dbo.MigratedAccounts (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    AccountID VARCHAR(50) NOT NULL,
    CustomerName VARCHAR(100) NOT NULL,
    RoutingNumber VARCHAR(20) NULL,
    Balance DECIMAL(18,2) NOT NULL,
    AccountType VARCHAR(50) NULL,
    MigratedOn DATETIME DEFAULT GETDATE()
);
GO
