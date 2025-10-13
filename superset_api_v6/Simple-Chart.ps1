# Simple PowerShell script for Superset chart creation
# Just the POST call - no complications

$BASE_URL = "http://localhost:8080"
$API_BASE = "$BASE_URL/api/v1"
$BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNzYwMzg5NTEzLCJqdGkiOiI0YmUwNTIzNi1lN2FmLTRjZmMtODUxYS03MzRkNzBkYmQ1MGIiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiMSIsIm5iZiI6MTc2MDM4OTUxMywiY3NyZiI6IjkyNGE3MjgzLTVmOWMtNDc5MS1iNGU4LWFiMzJiNzZjOWFmMiIsImV4cCI6MTc2MDM5MDQxM30.MBznTLUImRLbcSvN9snfUvpGBTZshddpLKwZ2e6K8yE"

$headers = @{
    "Authorization" = "Bearer $BEARER_TOKEN"
    "Content-Type" = "application/json"
}

$body = @{
    "datasource_id" = 17
    "datasource_type" = "table"
    "slice_name" = "PowerShell Simple Test"
    "viz_type" = "table"
    "params" = '{"datasource":{"id":17,"type":"table"},"viz_type":"table","adhoc_filters":[],"all_columns":["date","daily_members_posting_messages"],"row_limit":100}'
} | ConvertTo-Json

Write-Host "Making POST request..."

try {
    $response = Invoke-RestMethod -Uri "$API_BASE/chart/" -Method POST -Body $body -Headers $headers
    Write-Host "SUCCESS! Chart ID: $($response.id)"
    Write-Host "URL: $BASE_URL/explore/?slice_id=$($response.id)"
} catch {
    Write-Host "FAILED: $($_.Exception.Message)"
}