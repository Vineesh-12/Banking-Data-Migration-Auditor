# =======================================================================================
# Phase 5: Final Integration & Scheduling
# Description: This script sets up a Windows Scheduled Task to run the Data Migration 
#              Auditor automatically every day at 5:00 PM.
# =======================================================================================

$TaskName = "BankingDataMigrationAudit"
$ActionPath = "dotnet"

# Assuming you have built the .NET project, point this to the compiled DLL or EXE
# For running via dotnet run (useful for development):
$ActionArguments = "run --project .\Phase3_Automation\DataMigrationAuditor.csproj"
$WorkingDirectory = $PSScriptRoot + "\.."

Write-Host "Creating Scheduled Task: $TaskName"
Write-Host "This will run the C# Auditor daily at 5:00 PM."

# 1. Define the trigger (Daily at 5:00 PM)
$Trigger = New-ScheduledTaskTrigger -Daily -At 5:00PM

# 2. Define the action (Run the .NET app)
$Action = New-ScheduledTaskAction -Execute $ActionPath -Argument $ActionArguments -WorkingDirectory $WorkingDirectory

# 3. Register the task in Windows Task Scheduler
try {
    Register-ScheduledTask -TaskName $TaskName -Trigger $Trigger -Action $Action -Description "Automated Audit of Banking Migration Data" -Force
    Write-Host "Task successfully scheduled! You can view it in the Windows Task Scheduler under '$TaskName'." -ForegroundColor Green
}
catch {
    Write-Host "Failed to register scheduled task. Ensure you are running PowerShell as Administrator." -ForegroundColor Red
    Write-Host $_.Exception.Message
}
