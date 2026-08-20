USE BankingAuditDB;
GO

IF OBJECT_ID('dbo.sp_AuditMigrationData', 'P') IS NOT NULL
BEGIN
    DROP PROCEDURE dbo.sp_AuditMigrationData;
END
GO

CREATE PROCEDURE dbo.sp_AuditMigrationData
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        Id,
        AccountID,
        CustomerName,
        RoutingNumber,
        Balance,
        AccountType,
        MigratedOn,
        CASE
            WHEN Balance < 0 THEN 'Error: Negative Balance'
            WHEN RoutingNumber IS NULL OR LTRIM(RTRIM(RoutingNumber)) = '' THEN 'Error: Missing/Blank Routing Number'
            WHEN AccountType IS NULL THEN 'Error: Missing Account Type'
            WHEN Balance > 10000000 THEN 'Warning: Unusually High Balance - Needs Review'
            WHEN AccountID IN (
                SELECT AccountID 
                FROM dbo.MigratedAccounts 
                GROUP BY AccountID 
                HAVING COUNT(*) > 1
            ) THEN 'Error: Duplicate Account ID Detected'
            ELSE 'Unknown Error'
        END AS IssueDescription
    FROM 
        dbo.MigratedAccounts
    WHERE 
        Balance < 0
        OR RoutingNumber IS NULL
        OR LTRIM(RTRIM(RoutingNumber)) = ''
        OR AccountType IS NULL
        OR Balance > 10000000
        OR AccountID IN (
            SELECT AccountID 
            FROM dbo.MigratedAccounts 
            GROUP BY AccountID 
            HAVING COUNT(*) > 1
        );
END
GO
