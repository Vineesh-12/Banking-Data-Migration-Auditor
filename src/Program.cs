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
            Console.WriteLine("Starting migration audit...");

            string connectionString = "Server=localhost\\SQLEXPRESS;Database=BankingAuditDB;Trusted_Connection=True;Encrypt=False;";
            string exportFilePath = "migration_errors.csv";

            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();
                    Console.WriteLine("DB connected.");

                    using (SqlCommand command = new SqlCommand("dbo.sp_AuditMigrationData", connection))
                    {
                        command.CommandType = CommandType.StoredProcedure;

                        using (SqlDataReader reader = command.ExecuteReader())
                        {
                            if (reader.HasRows)
                            {
                                using (StreamWriter file = new StreamWriter(exportFilePath, false, Encoding.UTF8))
                                {
                                    string[] headers = { "Id", "AccountID", "CustomerName", "RoutingNumber", "Balance", "AccountType", "IssueDescription" };
                                    file.WriteLine(string.Join(",", headers));

                                    int errorCount = 0;
                                    while (reader.Read())
                                    {
                                        string[] row = {
                                            reader["Id"].ToString(),
                                            reader["AccountID"].ToString(),
                                            reader["CustomerName"].ToString().Replace(",", ""), 
                                            reader["RoutingNumber"].ToString(),
                                            reader["Balance"].ToString(),
                                            reader["AccountType"].ToString(),
                                            reader["IssueDescription"].ToString().Replace(",", " -")
                                        };
                                        file.WriteLine(string.Join(",", row));
                                        errorCount++;
                                    }
                                    Console.WriteLine($"Audit finished. {errorCount} errors found.");
                                    Console.WriteLine($"Exported to: {exportFilePath}");
                                    
                                    RunPythonAnalysisScript();
                                }
                            }
                            else
                            {
                                Console.WriteLine("Audit finished. No errors found.");
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error during audit: {ex.Message}");
            }
        }

        static void RunPythonAnalysisScript()
        {
            Console.WriteLine("Running python analysis...");
            try
            {
                string pythonScriptPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "..", "..", "scripts", "analyze_errors.py");
                
                if (!File.Exists(pythonScriptPath)) 
                {
                    pythonScriptPath = Path.Combine("..", "scripts", "analyze_errors.py");
                }

                System.Diagnostics.ProcessStartInfo start = new System.Diagnostics.ProcessStartInfo();
                start.FileName = "python";
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
                Console.WriteLine($"Failed to run python script: {ex.Message}");
            }
        }
    }
}
