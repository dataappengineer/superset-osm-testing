# Superset Dataset Creation Test Script  
# Tests dataset creation API with current SQLite setup

# Configuration
$SupersetUrl = "http://localhost:8080"
$Username = "admin"
$Password = "admin"

Write-Host "Starting Superset Dataset Creation Test..." -ForegroundColor Yellow
Write-Host "Superset URL: $SupersetUrl" -ForegroundColor Gray

# Get fresh access token
Write-Host "`nAuthenticating..." -ForegroundColor Yellow

$loginBody = @{
    username = $Username
    password = $Password
    provider = "db"
    refresh = $true
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "$SupersetUrl/api/v1/security/login" -Method POST -Body $loginBody -ContentType "application/json"
    $accessToken = $loginResponse.access_token
    Write-Host "Authentication successful!" -ForegroundColor Green
} catch {
    Write-Host "Authentication failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type" = "application/json"
}

# First, let's see available databases
Write-Host "`nGetting available databases..." -ForegroundColor Yellow
try {
    $databases = Invoke-RestMethod -Uri "$SupersetUrl/api/v1/database/" -Headers $headers
    Write-Host "Available databases:" -ForegroundColor Green
    foreach ($db in $databases.result) {
        Write-Host "  - ID: $($db.id) | Name: $($db.database_name) | Backend: $($db.backend)" -ForegroundColor White
    }
    
    # Use the first available database (usually examples/SQLite)
    $databaseId = $databases.result[0].id
    $databaseName = $databases.result[0].database_name
    Write-Host "`nUsing Database: ID=$databaseId, Name=$databaseName" -ForegroundColor Cyan
    
} catch {
    Write-Host "Failed to get databases: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Get available tables in the database
Write-Host "`nGetting available tables..." -ForegroundColor Yellow
try {
    # Try the correct endpoint for getting table schemas
    $tablesUrl = "$SupersetUrl/api/v1/database/$databaseId/table_metadata/"
    $tables = Invoke-RestMethod -Uri $tablesUrl -Headers $headers
    Write-Host "Available tables in $databaseName database:" -ForegroundColor Green
    
    if ($tables.result) {
        $availableTables = $tables.result | Select-Object -First 10
        foreach ($table in $availableTables) {
            Write-Host "  - $table" -ForegroundColor White
        }
        # Use the first available table
        $tableName = $availableTables[0]
    } else {
        # Fallback to a known table
        $tableName = "birth_names"
        Write-Host "  - Using fallback table: $tableName" -ForegroundColor White
    }
    
    Write-Host "`nUsing Table: $tableName" -ForegroundColor Cyan
    
} catch {
    Write-Host "Failed to get tables: $($_.Exception.Message)" -ForegroundColor Yellow
    # Use a known table from Superset examples
    $tableName = "birth_names"
    Write-Host "Using default table: $tableName" -ForegroundColor Cyan
}

$timestamp = Get-Date -Format 'HHmmss'

# Test dataset creation via API - using a specific table
Write-Host "`nCreating dataset via API..." -ForegroundColor Yellow

# Let's try creating a dataset from a specific table that we know exists
$specificTable = "birth_names"  # This is a common table in Superset examples

$datasetData = @{
    database = $databaseId
    table_name = $specificTable
    schema = $null  # SQLite doesn't use schemas typically
    owners = @(1)   # Admin user
} | ConvertTo-Json -Depth 10

try {
    Write-Host "Attempting to create dataset for table: $specificTable" -ForegroundColor Cyan
    $datasetResponse = Invoke-RestMethod -Uri "$SupersetUrl/api/v1/dataset/" -Method POST -Headers $headers -Body $datasetData
    
    Write-Host "SUCCESS: Dataset created!" -ForegroundColor Green
    Write-Host "Dataset ID: $($datasetResponse.id)" -ForegroundColor Green
    Write-Host "Dataset Name: $specificTable" -ForegroundColor Green
    Write-Host "Database: $databaseName (ID: $databaseId)" -ForegroundColor Green
    
    # Get the created dataset details
    Write-Host "`nGetting dataset details..." -ForegroundColor Yellow
    $datasetDetails = Invoke-RestMethod -Uri "$SupersetUrl/api/v1/dataset/$($datasetResponse.id)" -Headers $headers
    
    Write-Host "Dataset Details:" -ForegroundColor Cyan
    Write-Host "  - Dataset ID: $($datasetDetails.result.id)" -ForegroundColor White
    Write-Host "  - Table Name: $($datasetDetails.result.table_name)" -ForegroundColor White
    Write-Host "  - Database ID: $($datasetDetails.result.database.id)" -ForegroundColor White
    Write-Host "  - Database Name: $($datasetDetails.result.database.database_name)" -ForegroundColor White
    Write-Host "  - Schema: $($datasetDetails.result.schema)" -ForegroundColor White
    Write-Host "  - SQL: $($datasetDetails.result.sql)" -ForegroundColor White
    Write-Host "  - Columns Count: $($datasetDetails.result.columns.Count)" -ForegroundColor White
    Write-Host "  - Metrics Count: $($datasetDetails.result.metrics.Count)" -ForegroundColor White
    
    if ($datasetDetails.result.columns.Count -gt 0) {
        Write-Host "`nFirst 5 columns:" -ForegroundColor Yellow
        $datasetDetails.result.columns | Select-Object -First 5 | ForEach-Object {
            Write-Host "    - $($_.column_name) ($($_.type)) - Groupable: $($_.groupby)" -ForegroundColor Gray
        }
    }
    
    if ($datasetDetails.result.metrics.Count -gt 0) {
        Write-Host "`nAvailable metrics:" -ForegroundColor Yellow
        $datasetDetails.result.metrics | ForEach-Object {
            Write-Host "    - $($_.metric_name): $($_.expression)" -ForegroundColor Gray
        }
    }
    
} catch {
    Write-Host "FAILED to create dataset: $($_.Exception.Message)" -ForegroundColor Red
    
    # Try to get more detailed error information
    if ($_.Exception.Response) {
        try {
            $errorStream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($errorStream)
            $errorBody = $reader.ReadToEnd()
            Write-Host "Error details: $errorBody" -ForegroundColor Red
        } catch {
            Write-Host "Could not read error details" -ForegroundColor Red
        }
    }
    
    # If the specific table doesn't work, try with the first available table
    Write-Host "`nTrying with first available table: $tableName" -ForegroundColor Yellow
    
    $fallbackData = @{
        database = $databaseId
        table_name = $tableName
        schema = $null
        owners = @(1)
    } | ConvertTo-Json -Depth 10
    
    try {
        $fallbackResponse = Invoke-RestMethod -Uri "$SupersetUrl/api/v1/dataset/" -Method POST -Headers $headers -Body $fallbackData
        Write-Host "SUCCESS with fallback: Dataset created with ID $($fallbackResponse.id)" -ForegroundColor Green
    } catch {
        Write-Host "Fallback also failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nTest completed at $(Get-Date)" -ForegroundColor Cyan

# Show the API call structure for future reference
Write-Host "`n" -ForegroundColor White
Write-Host "=== API CALL STRUCTURE FOR FUTURE REFERENCE ===" -ForegroundColor Yellow
Write-Host "Current (SQLite):" -ForegroundColor Cyan
Write-Host "  Database ID: $databaseId (examples/SQLite)" -ForegroundColor White
Write-Host "  Table: $tableName" -ForegroundColor White
Write-Host ""
Write-Host "Future (Dremio):" -ForegroundColor Cyan  
Write-Host "  Database ID: [New Dremio Connection ID]" -ForegroundColor White
Write-Host "  Table: mongo.your_collection OR postgres.your_table" -ForegroundColor White
Write-Host ""
Write-Host "API Body Structure (IDENTICAL):" -ForegroundColor Yellow
Write-Host @"
{
  "database": [database_id],
  "table_name": "[table_or_collection_name]", 
  "schema": null,
  "owners": [1]
}
"@ -ForegroundColor Gray