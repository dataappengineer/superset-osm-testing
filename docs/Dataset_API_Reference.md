# 📊 Riferimento API per Creazione Dataset Superset

## 🎯 Obiettivo
Documentazione dettagliata dei parametri API e esempi pratici per la creazione e gestione di dataset in Superset tramite chiamate REST.

> 📋 **Stato Validazione**: **Dataset API completamente validata e testata** con Superset v6
> - ✅ GET Dataset Details (lettura completa struttura dataset)
> - ✅ POST Dataset Creation (creazione nuovo dataset da tabelle database)  
> - ✅ Dataset Structure Analysis (analisi colonne, metriche, e configurazioni)
> - ✅ Database Connection Management (gestione connessioni database)

---

## 📑 Indice

- [🔑 Autenticazione](#-autenticazione)
- [🔍 Ottenere l'ID del Dataset Creato](#-ottenere-lid-del-dataset-creato)
- [📋 Lettura Dataset Esistente](#-lettura-dataset-esistente)
- [🗄️ Creazione Dataset](#️-creazione-dataset)
- [🏗️ Struttura Dataset Response](#️-struttura-dataset-response)
- [🔧 Gestione Database Connections](#-gestione-database-connections)

---

## 🔑 Autenticazione

Prima di effettuare qualsiasi chiamata alle API di Superset, è necessario autenticarsi per ottenere un token JWT.

**Endpoint:**  
`POST /api/v1/security/login`

**Body:**
```json
{
  "username": "NOME_UTENTE",
  "password": "PASSWORD",
  "provider": "db",
  "refresh": true
}
```

**Risposta:**  
Riceverai un oggetto JSON con il token di accesso (`access_token`).  
**Esempio header da usare nelle chiamate successive:**
```
Authorization: Bearer <access_token>
```

---

## 🔍 Ottenere l'ID del Dataset Creato

Dopo ogni chiamata `POST /api/v1/dataset/` con successo, la risposta contiene l'**ID del dataset appena creato**:

**Struttura risposta di successo:**
```json
{
  "id": 24,
  "result": {
    "id": 24,
    "table_name": "users_channels",
    "database": {
      "id": 1,
      "database_name": "examples",
      "backend": "sqlite"
    },
    "schema": "main",
    "sql": null,
    "datasource_type": "table",
    "columns": [...],
    "metrics": [...],
    "created_on": "2025-10-09T23:29:11.829002",
    "changed_on": "2025-10-15T16:25:58.582674"
  }
}
```

**Come estrarre l'ID:**
- L'**ID principale** si trova nel campo `id` a livello root della risposta
- È anche disponibile in `result.id` (stesso valore)
- Questo ID può essere utilizzato per operazioni successive come:
  - Modifica dataset: `PUT /api/v1/dataset/{id}`
  - Cancellazione: `DELETE /api/v1/dataset/{id}`
  - Ottenere dettagli: `GET /api/v1/dataset/{id}`
  - **Creazione chart**: Usare come `datasource_id` nelle chiamate chart

**Esempio di estrazione ID (PowerShell):**
```powershell
$response = Invoke-RestMethod -Uri "$SupersetUrl/api/v1/dataset/" -Method POST -Headers $headers -Body $jsonBody -ContentType "application/json"
$datasetId = $response.id
Write-Host "Dataset creato con ID: $datasetId"
# Ora puoi usare $datasetId come datasource_id per creare chart
```

---

## 📋 Lettura Dataset Esistente

### Endpoint per Dettagli Dataset

**Endpoint:**  
`GET /api/v1/dataset/{dataset_id}`

**Parametri:**
- `dataset_id`: ID numerico del dataset (**obbligatorio**)

**Esempio di chiamata:**
```powershell
$datasetDetails = Invoke-RestMethod -Uri "$SupersetUrl/api/v1/dataset/24" -Headers $headers
```

**Risposta Completa:**
La risposta contiene tutti i dettagli necessari per utilizzare il dataset:

```json
{
  "result": {
    "id": 24,
    "table_name": "users_channels",
    "datasource_name": "users_channels",
    "datasource_type": "table",
    "database": {
      "id": 1,
      "database_name": "examples",
      "backend": "sqlite",
      "allow_multi_catalog": false
    },
    "schema": "main",
    "sql": null,
    "columns": [
      {
        "id": 762,
        "column_name": "user_id",
        "type": "STRING",
        "groupby": true,
        "filterable": true,
        "is_dttm": false
      },
      {
        "id": 763,
        "column_name": "name", 
        "type": "STRING",
        "groupby": true,
        "filterable": true,
        "is_dttm": false
      }
    ],
    "metrics": [
      {
        "id": 31,
        "metric_name": "count",
        "expression": "count(*)",
        "metric_type": null
      }
    ]
  }
}
```

---

## 🗄️ Creazione Dataset

### Metodo di Creazione Dataset

**Endpoint:**  
`POST /api/v1/dataset/`

**Parametri indispensabili:**
- `database`: ID numerico del database connection (**obbligatorio**)
- `table_name`: Nome della tabella nel database (**obbligatorio**)
- `schema`: Nome dello schema (può essere null per SQLite) (**opzionale**)
- `owners`: Array con ID degli owner (es. [1]) (**opzionale**)

**Esempio creazione base:**
```json
{
  "database": 1,
  "table_name": "users_channels",
  "schema": null,
  "owners": [1]
}
```

### Workflow Creazione Dataset

**Step 1: Ottenere Database ID**
```powershell
$databases = Invoke-RestMethod -Uri "$SupersetUrl/api/v1/database/" -Headers $headers
# Seleziona il database desiderato
$databaseId = $databases.result[0].id
```

**Step 2: Creare Dataset**
```powershell
$datasetData = @{
    database = $databaseId
    table_name = "nome_tabella"
    schema = $null
    owners = @(1)
} | ConvertTo-Json

$datasetResponse = Invoke-RestMethod -Uri "$SupersetUrl/api/v1/dataset/" -Method POST -Headers $headers -Body $datasetData -ContentType "application/json"
```

**Step 3: Ottenere Dataset ID per Chart**
```powershell
$datasetId = $datasetResponse.id
# Usa questo ID come datasource_id nei chart
```

---

## 🏗️ Struttura Dataset Response

### Campi Principali

**Identificazione:**
- `id`: ID numerico del dataset (usare per chart)
- `table_name`: Nome tabella originale
- `datasource_name`: Nome completo dataset
- `datasource_type`: Sempre "table"

**Database Connection:**
- `database.id`: ID connection database
- `database.database_name`: Nome database
- `database.backend`: Tipo database (sqlite, postgresql, etc.)

**Schema e Struttura:**
- `schema`: Schema database (può essere null)
- `sql`: Query SQL personalizzata (null per tabelle fisiche)
- `kind`: "physical" per tabelle, "virtual" per viste SQL

**Colonne Disponibili:**
```json
"columns": [
  {
    "id": 762,
    "column_name": "user_id",
    "type": "STRING",
    "groupby": true,     // Usabile per raggruppamenti
    "filterable": true,  // Usabile per filtri
    "is_dttm": false     // È colonna temporale
  }
]
```

**Metriche Disponibili:**
```json
"metrics": [
  {
    "id": 31,
    "metric_name": "count",
    "expression": "count(*)",
    "metric_type": null
  }
]
```

---

## 🔧 Gestione Database Connections

### Ottenere Database Disponibili

**Endpoint:**  
`GET /api/v1/database/`

**Esempio:**
```powershell
$databases = Invoke-RestMethod -Uri "$SupersetUrl/api/v1/database/" -Headers $headers
foreach ($db in $databases.result) {
    Write-Host "ID: $($db.id) | Name: $($db.database_name) | Backend: $($db.backend)"
}
```

### Differenze per Tipo Database

**SQLite (Current Setup):**
```json
{
  "database": 1,
  "table_name": "birth_names",
  "schema": null
}
```

**Dremio + MongoDB (Future Setup):**
```json
{
  "database": 2,
  "table_name": "mongo.mydb.collection_name",
  "schema": null
}
```

**Dremio + PostgreSQL (Future Setup):**
```json
{
  "database": 3,
  "table_name": "postgres.public.table_name", 
  "schema": "public"
}
```

---

## ⚠️ Note Tecniche Importanti

### Limitazioni API
- **Tabelle Esistenti**: Il dataset deve riferirsi a una tabella che esiste nel database
- **Permessi**: L'utente deve avere permessi sul database connection
- **Duplicati**: Creare dataset per la stessa tabella può causare errori

### Best Practices
1. **Verificare Database Connection**: Assicurarsi che il database sia attivo
2. **Controllare Tabelle**: Verificare che la tabella esista prima di creare dataset
3. **Gestire Errori**: Le API restituiscono 422 per dati non validi
4. **ID Dataset**: Salvare l'ID del dataset per usarlo nei chart

### Workflow Consigliato
1. Autenticarsi con `POST /api/v1/security/login`
2. Ottenere database disponibili con `GET /api/v1/database/`
3. Creare dataset con `POST /api/v1/dataset/`
4. Usare dataset ID come `datasource_id` nei chart
5. Verificare dataset con `GET /api/v1/dataset/{id}`

---

## 🔍 Script di Esempio

### Get-Dataset-Details.ps1
Script per analizzare struttura dataset esistente:
```powershell
.\Get-Dataset-Details.ps1 -DatasetId 24
```

### Test-Dataset-Creation.ps1  
Script per creare nuovo dataset:
```powershell
.\Test-Dataset-Creation.ps1
```

**Output esempio:**
```
SUCCESS: Dataset created!
Dataset ID: 25
Dataset Name: users_channels
Database: examples (ID: 1)
Columns Count: 2
Available metrics: count: count(*)
```

---

## 🔄 Integrazione con Chart API

### Usare Dataset ID nei Chart

Una volta creato il dataset, usa l'ID per creare chart:

```json
{
  "datasource_id": 24,        // ID del dataset creato
  "datasource_type": "table",
  "slice_name": "Mio Chart",
  "viz_type": "table",
  "params": "{\"datasource\":{\"id\":24,\"type\":\"table\"},\"viz_type\":\"table\",\"all_columns\":[\"user_id\",\"name\"],\"row_limit\":100}"
}
```

### Colonne e Metriche Disponibili

Usa le informazioni del dataset per costruire chart validi:
- **Colonne**: Usa `column_name` delle colonne con `groupby: true`
- **Metriche**: Usa `metric_name` delle metriche disponibili
- **Filtri**: Usa colonne con `filterable: true`

---

> 📋 **Conclusione**: L'API dataset di Superset v6 permette creazione programmatica di dataset da qualsiasi database connesso. Il dataset ID ottenuto viene utilizzato come `datasource_id` per creare chart tramite l'API chart.