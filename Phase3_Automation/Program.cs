using System;
using System.Data;
using System.IO;
using Microsoft.Data.SqlClient;
using System.Text;

namespace DataMigrationAuditor
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Starting Data Migration Audit...");

            // Connection string for local SQL Server Express (Update if needed)
            string connectionString = "Server=localhost\\SQLEXPRESS;Database=BankingAuditDB;Trusted_Connection=True;Encrypt=False;";
            string exportFilePath = "migration_errors.csv";

            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();
                    Console.WriteLine("Connected to BankingAuditDB successfully.");

                    using (SqlCommand command = new SqlCommand("dbo.sp_AuditMigrationData", connection))
                    {
                        command.CommandType = CommandType.StoredProcedure;

                        using (SqlDataReader reader = command.ExecuteReader())
                        {
                            if (reader.HasRows)
                            {
                                // Write to CSV
                                using (StreamWriter file = new StreamWriter(exportFilePath, false, Encoding.UTF8))
                                {
                                    // Write Headers
                                    string[] headers = { "Id", "AccountID", "CustomerName", "RoutingNumber", "Balance", "AccountType", "IssueDescription" };
                                    file.WriteLine(string.Join(",", headers));

                                    int errorCount = 0;
                                    while (reader.Read())
                                    {
                                        string[] row = {
                                            reader["Id"].ToString(),
                                            reader["AccountID"].ToString(),
                                            reader["CustomerName"].ToString().Replace(",", ""), // Basic sanitization
                                            reader["RoutingNumber"].ToString(),
                                            reader["Balance"].ToString(),
                                            reader["AccountType"].ToString(),
                                            reader["IssueDescription"].ToString().Replace(",", " -") // Sanitize commas for CSV
                                        };
                                        file.WriteLine(string.Join(",", row));
                                        errorCount++;
                                    }
                                    Console.WriteLine($"Audit complete! Found {errorCount} errors.");
                                    Console.WriteLine($"Errors exported to: {exportFilePath}");
                                }
                            }
                            else
                            {
                                Console.WriteLine("Audit complete. No migration errors found!");
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("An error occurred during the audit process:");
                Console.WriteLine(ex.Message);
            }
        }
    }
}
