$TaskName = "BankingDataMigrationAudit"
$ActionPath = "dotnet"
$ActionArguments = "run --project .\src\DataMigrationAuditor.csproj"
$WorkingDirectory = $PSScriptRoot + "\.."

Write-Host "Creating task $TaskName..."

$Trigger = New-ScheduledTaskTrigger -Daily -At 5:00PM
$Action = New-ScheduledTaskAction -Execute $ActionPath -Argument $ActionArguments -WorkingDirectory $WorkingDirectory

try {
    Register-ScheduledTask -TaskName $TaskName -Trigger $Trigger -Action $Action -Description "Automated Audit of Banking Migration Data" -Force
    Write-Host "Task scheduled successfully." -ForegroundColor Green
}
catch {
    Write-Host "Failed to register task. Run as Administrator." -ForegroundColor Red
    Write-Host $_.Exception.Message
}
