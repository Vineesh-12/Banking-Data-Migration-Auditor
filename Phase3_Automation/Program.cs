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
                                    
                                    // Phase 5 Integration: Automatically run the Python analysis script
                                    RunPythonAnalysisScript();
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

        static void RunPythonAnalysisScript()
        {
            Console.WriteLine("Triggering Python data analysis script...");
            try
            {
                // The python script is located in the Phase4 folder relative to the executable
                string pythonScriptPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "..", "..", "Phase4_DataAnalysis", "analyze_errors.py");
                
                // Fallback for simple execution
                if (!File.Exists(pythonScriptPath)) 
                {
                    pythonScriptPath = Path.Combine("..", "Phase4_DataAnalysis", "analyze_errors.py");
                }

                System.Diagnostics.ProcessStartInfo start = new System.Diagnostics.ProcessStartInfo();
                start.FileName = "python"; // Assumes python is in the system PATH
                start.Arguments = $"\"{pythonScriptPath}\"";
                start.UseShellExecute = false;
                start.RedirectStandardOutput = true;
                
                using (System.Diagnostics.Process process = System.Diagnostics.Process.Start(start))
                {
                    using (StreamReader reader = process.StandardOutput)
                    {
                        string result = reader.ReadToEnd();
                        Console.WriteLine(result);
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Failed to execute Python script. Ensure Python is installed and in your PATH.");
                Console.WriteLine(ex.Message);
            }
        }
    }
}
