
# 📊 Riferimento API per Creazione Chart Superset

## 🎯 Obiettivo
Documentazione dettagliata dei parametri API e esempi pratici per la creazione automatica di chart e dashboard in Superset tramite chiamate REST.

> 📋 **Stato Validazione**: **9 tipi di chart completamente validati e testati** con Superset v6 API
> - ✅ Table (RAW e AGGREGATE)
> - ✅ Pivot Table (ROWS e COLUMNS) 
> - ✅ Bar Chart (echarts_timeseries_bar) - **Versione Corretta con Dataset Specifico**
> - ✅ Pie Chart
> - ✅ Line Chart (echarts_timeseries_line)
> - ✅ Heat Map (heatmap_v2)
> - ✅ Tree Chart (tree_chart)
> - ✅ Scatter Plot (echarts_timeseries_scatter)
> - ✅ Big Number (big_number_total)

---
## 📑 Indice

- [🔑 Autenticazione (comune a tutte le chiamate)](#-autenticazione-comune-a-tutte-le-chiamate)
- [📋 Creazione Chart](#-creazione-chart)
  - [1. Table - Tabella Base](#1-table---tabella-base)
  - [2. Pivot Table - Tabella Pivot](#2-pivot-table---tabella-pivot)
  - [3. Bar Chart - Grafico a Barre](#3-bar-chart---grafico-a-barre)
  - [4. Pie Chart - Grafico a Torta](#4-pie-chart---grafico-a-torta)
  - [5. Line Chart - Grafico a Linee](#5-line-chart---grafico-a-linee)
  - [6. Heat Map - Mappa di Calore](#6-heat-map---mappa-di-calore)
  - [7. Tree Chart - Grafico ad Albero](#7-tree-chart---grafico-ad-albero)
  - [8. Scatter Plot - Grafico a Dispersione](#8-scatter-plot---grafico-a-dispersione)
  - [9. Big Number - Numero Grande](#9-big-number---numero-grande)
  - [🔧 Schema Base e Parametri Comuni](#-schema-base-della-richiesta-post-apiv1chart)
- [📊 Creazione Dashboard con Filtri](#-creazione-dashboard-con-filtri-tramite-api)
  - [📋 Panoramica e Parametri Obbligatori](#panoramica-e-parametri-obbligatori)
  - [🔄 Workflow delle Chiamate API](#workflow-delle-chiamate-api-per-la-creazione-di-dashboard)
  - [⚠️ Note Tecniche Importanti](#note-tecniche-importanti)
  - [🎯 Creazione della Dashboard (Step-by-Step)](#creazione-della-dashboard-step-by-step)
    - [Step 1: Creazione della Dashboard](#1-creazione-della-dashboard)
    - [Step 2: Esempi Parametri Obbligatori](#2-esempi-pratici-di-parametri-obbligatori)
    - [Step 3: Chiamata POST Completa](#3-esempio-completo-di-chiamata-post-apiv1dashboard)
    - [Step 4: Aggiornamento Posizione (Opzionale)](#4-opzionale-aggiornamento-posizione-grafici)
    - [Step 5: Associazione Grafici (Opzionale)](#5-opzionale-associazione-esplicita-dei-grafici-alla-dashboard)
    - [Step 6: Verifica Finale](#6-verifica-finale)
- [🗄️ Creazione Dataset](#-creazione-dataset)

---
## 🔑 Autenticazione (comune a tutte le chiamate)

Prima di effettuare qualsiasi chiamata alle API di Superset, è necessario autenticarsi per ottenere un token JWT. Questo token va incluso nell'header `Authorization` di tutte le richieste successive.

- **API_BASE**: URL base delle API REST di Superset (es: `http://localhost:8080/api/v1`)
- **Token di autenticazione**: Token JWT ottenuto tramite login (`/security/login`)

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

---
## 📋 Creazione Chart

### 1. **Table** - Tabella Base

**Endpoint:**  
`POST /api/v1/chart/`


**Modalità RAW** (per visualizzare record effettivi):

**Parametri indispensabili per Superset v6:**
- `datasource_id`: ID numerico del dataset (**obbligatorio**)
- `datasource_type`: "table" (**obbligatorio**)
- `slice_name`: Nome del chart (**obbligatorio**)
- `viz_type`: "table" (**obbligatorio**)
- `params`: Stringa JSON con configurazione chart (**obbligatorio**)

**API d'esempio (v6) - versione validata e funzionante**:
```json
{
  "datasource_id": DATASET_ID,
  "datasource_type": "table",
  "slice_name": "Nome del Chart",
  "viz_type": "table",
  "params": "{\"datasource\":{\"id\":DATASET_ID,\"type\":\"table\"},\"viz_type\":\"table\",\"adhoc_filters\":[],\"all_columns\":[\"colonna1\",\"colonna2\",\"colonna3\"],\"row_limit\":100}"
}
```

> ⚠️ **IMPORTANTE per v6:**
> - Il campo `params` deve essere una **stringa JSON**, non un oggetto JSON
> - Il campo `datasource` dentro params usa la struttura `{"id": NUMBER, "type": "table"}`

**Parametri opzionali in params (v6):**
- `adhoc_filters`: Filtri sui dati in formato array (default: [])
  - **Formato corretto v6**: `[{"expressionType":"SIMPLE","subject":"colonna","operator":">","comparator":100,"clause":"WHERE"}]`
  - Operatori: `>`, `<`, `>=`, `<=`, `==`, `!=`
- `row_limit`: Numero massimo di righe (default: 100)

**Esempio validato con filtro (FUNZIONANTE):**
```json
{
  "datasource_id": 17,
  "datasource_type": "table",
  "slice_name": "Table RAW with Filter",
  "viz_type": "table",
  "params": "{\"datasource\":{\"id\":17,\"type\":\"table\"},\"viz_type\":\"table\",\"adhoc_filters\":[{\"expressionType\":\"SIMPLE\",\"subject\":\"daily_members_posting_messages\",\"operator\":\">\",\"comparator\":1,\"clause\":\"WHERE\"}],\"all_columns\":[\"date\",\"daily_members_posting_messages\"],\"row_limit\":100}"
}
```


> 📝 **NOTA su datasource v6:**
> - L'ID numerico deve corrispondere al dataset esistente in Superset
> - La risposta includerà l'ID del chart creato per riferimenti futuri

> **Modalità AGGREGATE:**
>

**Modalità AGGREGATE** (per metriche aggregate):

**Parametri indispensabili:**
- `query_mode`: "aggregate" (**obbligatorio**)
- `groupby`: Colonne per raggruppamento (es. ["date"]) (**obbligatorio**)
- `metrics`: Metriche aggregate (es. ["count"]) (**obbligatorio**)

**Esempio validato AGGREGATE (FUNZIONANTE):**
```json
{
  "datasource_id": 17,
  "datasource_type": "table",
  "slice_name": "Table AGGREGATE",
  "viz_type": "table",
  "params": "{\"datasource\":{\"id\":17,\"type\":\"table\"},\"viz_type\":\"table\",\"query_mode\":\"aggregate\",\"groupby\":[\"date\"],\"metrics\":[\"count\"],\"adhoc_filters\":[],\"row_limit\":100,\"order_desc\":true}"
}
```

---

### 2. **Pivot Table** - Tabella Pivot

**Endpoint:** `POST /api/v1/chart/`

**Parametri indispensabili:**
- `datasource_id`: ID numerico del dataset (**obbligatorio**)
- `datasource_type`: "table" (**obbligatorio**)
- `slice_name`: Nome del chart (**obbligatorio**)
- `viz_type`: "pivot_table_v2" (**obbligatorio**)
- `params`: Stringa JSON con configurazione (**obbligatorio**)

**Parametri chiave in params:**
- `groupbyRows`: Righe della pivot (es. ["date"])
- `groupbyColumns`: Colonne della pivot (es. [])
- `metrics`: Metriche (es. ["count"])
- `metricsLayout`: "ROWS" o "COLUMNS" per disposizione metriche

**Esempio PIVOT - Metrics on ROWS (FUNZIONANTE):**
```json
{
  "datasource_id": 17,
  "datasource_type": "table",
  "slice_name": "Pivot Table (Metrics on ROWS)",
  "viz_type": "pivot_table_v2",
  "params": "{\"datasource\":{\"id\":17,\"type\":\"table\"},\"viz_type\":\"pivot_table_v2\",\"groupbyRows\":[\"date\"],\"groupbyColumns\":[],\"metrics\":[\"count\"],\"metricsLayout\":\"ROWS\",\"adhoc_filters\":[],\"row_limit\":10000,\"aggregateFunction\":\"Sum\"}"
}
```

**Esempio PIVOT - Metrics on COLUMNS (FUNZIONANTE):**
```json
{
  "datasource_id": 17,
  "datasource_type": "table",
  "slice_name": "Pivot Table (Metrics on COLUMNS)",
  "viz_type": "pivot_table_v2",
  "params": "{\"datasource\":{\"id\":17,\"type\":\"table\"},\"viz_type\":\"pivot_table_v2\",\"groupbyRows\":[],\"groupbyColumns\":[\"date\"],\"metrics\":[\"count\"],\"metricsLayout\":\"COLUMNS\",\"adhoc_filters\":[],\"row_limit\":10000,\"aggregateFunction\":\"Sum\"}"
}
```


### 3. **Bar Chart** - Grafico a Barre

**Endpoint:** `POST /api/v1/chart/`

**Parametri indispensabili:**
- `datasource_id`: ID numerico del dataset (**obbligatorio**)
- `datasource_type`: "table" (**obbligatorio**)
- `slice_name`: Nome del chart (**obbligatorio**)
- `viz_type`: "echarts_timeseries_bar" (**obbligatorio**)
- `params`: Stringa JSON con configurazione (**obbligatorio**)

**Parametri chiave in params:**
- `x_axis`: Colonna per asse X (es. "order_date")
- `metrics`: Metriche per asse Y (es. ["count"])
- `groupby`: Raggrupamenti per serie (es. ["deal_size"])
- `time_grain_sqla`: Granularità temporale (es. "P1M")
- `orientation`: "vertical" o "horizontal"

**Esempio validato (FUNZIONANTE):**
```json
{
  "datasource_id": 9,
  "datasource_type": "table",
  "slice_name": "Bar Chart - Order Date vs Count by Deal Size",
  "viz_type": "echarts_timeseries_bar",
  "params": "{\"datasource\":{\"id\":9,\"type\":\"table\"},\"viz_type\":\"echarts_timeseries_bar\",\"x_axis\":\"order_date\",\"time_grain_sqla\":\"P1M\",\"x_axis_sort_asc\":true,\"x_axis_sort_series\":\"name\",\"x_axis_sort_series_ascending\":true,\"metrics\":[\"count\"],\"groupby\":[\"deal_size\"],\"adhoc_filters\":[{\"clause\":\"WHERE\",\"subject\":\"order_date\",\"operator\":\"TEMPORAL_RANGE\",\"comparator\":\"No filter\",\"expressionType\":\"SIMPLE\"}],\"order_desc\":true,\"row_limit\":10000,\"truncate_metric\":true,\"show_empty_columns\":true,\"comparison_type\":\"values\",\"annotation_layers\":[],\"forecastPeriods\":10,\"forecastInterval\":0.8,\"orientation\":\"vertical\",\"x_axis_title_margin\":15,\"y_axis_title_margin\":15,\"y_axis_title_position\":\"Left\",\"sort_series_type\":\"sum\",\"color_scheme\":\"supersetColors\",\"only_total\":true,\"show_legend\":true,\"legendType\":\"scroll\",\"legendOrientation\":\"top\",\"x_axis_time_format\":\"smart_date\",\"y_axis_format\":\"SMART_NUMBER\",\"truncateXAxis\":true,\"y_axis_bounds\":[null,null],\"rich_tooltip\":true,\"tooltipTimeFormat\":\"smart_date\",\"extra_form_data\":{},\"dashboards\":[]}"
}
```

> ⚠️ **IMPORTANTE per v6:**
> - Usare `viz_type`: "echarts_timeseries_bar" (non "dist_bar")
> - Il parametro principale è `x_axis` per l'asse X
> - Usare `groupby` per raggruppamenti/serie multiple
> - Il parametro `time_grain_sqla` controlla la granularità temporale
> - Il campo `params` deve essere una stringa JSON

---

### 4. **Pie Chart** - Grafico a Torta

**Endpoint:** `POST /api/v1/chart/`

**Parametri indispensabili:**
- `datasource_id`: ID numerico del dataset (**obbligatorio**)
- `datasource_type`: "table" (**obbligatorio**)
- `slice_name`: Nome del chart (**obbligatorio**)
- `viz_type`: "pie" (**obbligatorio**)
- `params`: Stringa JSON con configurazione (**obbligatorio**)

**Parametri chiave in params:**
- `groupby`: Colonne per categorie spicchi (es. ["date"])
- `metric`: Metrica singola per dimensioni (es. "count")
- `donut`: Stile ciambella (true/false)
- `show_labels`: Mostra etichette sui spicchi

**Esempio validato (FUNZIONANTE):**
```json
{
  "datasource_id": 17,
  "datasource_type": "table",
  "slice_name": "Pie Chart - Distribution by Date",
  "viz_type": "pie",
  "params": "{\"datasource\":{\"id\":17,\"type\":\"table\"},\"viz_type\":\"pie\",\"groupby\":[\"date\"],\"metric\":\"count\",\"adhoc_filters\":[],\"row_limit\":50,\"color_scheme\":\"bnbColors\",\"donut\":false,\"show_labels\":true,\"labels_outside\":false,\"outerRadius\":70,\"innerRadius\":30}"
}
```

> ⚠️ **IMPORTANTE per v6:**
> - Il parametro `metric` deve essere una stringa singola (non array)
> - Usare `groupby` per le categorie dei spicchi
> - Il campo `params` deve essere una stringa JSON

### 5. **Line Chart** - Grafico a Linee

**Endpoint:** `POST /api/v1/chart/`

**Parametri indispensabili:**
- `datasource_id`: ID numerico del dataset (**obbligatorio**)
- `datasource_type`: "table" (**obbligatorio**)
- `slice_name`: Nome del chart (**obbligatorio**)
- `viz_type`: "echarts_timeseries_line" (**obbligatorio**)
- `params`: Stringa JSON con configurazione (**obbligatorio**)

**Parametri chiave in params:**
- `granularity_sqla`: Colonna temporale per asse X (es. "date")
- `metrics`: Metriche per asse Y (es. ["count"])
- `groupby`: Raggrupamenti per serie multiple (es. [])
- `show_legend`: Mostra legenda
- `rich_tooltip`: Tooltip dettagliato

**Esempio validato (FUNZIONANTE):**
```json
{
  "datasource_id": 17,
  "datasource_type": "table",
  "slice_name": "Line Chart - Trend over Time",
  "viz_type": "echarts_timeseries_line",
  "params": "{\"datasource\":{\"id\":17,\"type\":\"table\"},\"viz_type\":\"echarts_timeseries_line\",\"granularity_sqla\":\"date\",\"metrics\":[\"count\"],\"groupby\":[],\"adhoc_filters\":[],\"row_limit\":1000,\"color_scheme\":\"bnbColors\",\"show_legend\":true,\"rich_tooltip\":true}"
}
```

> ⚠️ **IMPORTANTE per v6:**
> - Usare `viz_type`: "echarts_timeseries_line" 
> - Il parametro principale è `granularity_sqla` per l'asse temporale
> - Il campo `params` deve essere una stringa JSON

---

### 6. **Heat Map** - Mappa di Calore

**Endpoint:** `POST /api/v1/chart/`

**Parametri indispensabili:**
- `datasource_id`: ID numerico del dataset (**obbligatorio**)
- `datasource_type`: "table" (**obbligatorio**)
- `slice_name`: Nome del chart (**obbligatorio**)
- `viz_type`: "heatmap_v2" (**obbligatorio**)
- `params`: Stringa JSON con configurazione (**obbligatorio**)

**Parametri chiave in params:**
- `x_axis`: Colonna asse X (es. "product_line") (**obbligatorio**)
- `groupby`: Colonna asse Y (es. "deal_size") (**obbligatorio**)
- `metric`: Metrica per intensità colore (es. "count") (**obbligatorio**)

**Parametri opzionali (default disponibili):**
- `normalize_across`: Normalizzazione (default: "heatmap")
- `xscale_interval`: Intervallo scala X (default: -1)
- `yscale_interval`: Intervallo scala Y (default: -1)
- `legend_type`: Tipo legenda (default: "continuous")
- `linear_color_scheme`: Gradiente colori (default: "superset_seq_1")
- `left_margin`: Margine sinistro (default: "auto")
- `bottom_margin`: Margine inferiore (default: "auto")
- `value_bounds`: Limiti valori (default: [null, null])
- `y_axis_format`: Formato valori (default: "SMART_NUMBER")
- `x_axis_time_format`: Formato asse X temporale (default: "smart_date")
- `show_legend`: Mostra legenda (default: true)
- `show_percentage`: Mostra percentuali (default: true)
- `show_values`: Mostra valori (default: true)
- `row_limit`: Limite righe (default: 10000)

**Esempio validato (FUNZIONANTE):**
```json
{
  "datasource_id": 9,
  "datasource_type": "table",
  "slice_name": "Heat Map Example",
  "viz_type": "heatmap_v2",
  "params": "{\"datasource\":{\"id\":9,\"type\":\"table\"},\"viz_type\":\"heatmap_v2\",\"x_axis\":\"product_line\",\"time_grain_sqla\":\"P1D\",\"groupby\":\"deal_size\",\"metric\":\"count\",\"adhoc_filters\":[{\"clause\":\"WHERE\",\"subject\":\"order_date\",\"operator\":\"TEMPORAL_RANGE\",\"comparator\":\"No filter\",\"expressionType\":\"SIMPLE\"}],\"row_limit\":10000,\"sort_x_axis\":\"alpha_asc\",\"sort_y_axis\":\"alpha_asc\",\"normalize_across\":\"heatmap\",\"legend_type\":\"continuous\",\"linear_color_scheme\":\"superset_seq_1\",\"xscale_interval\":-1,\"yscale_interval\":-1,\"left_margin\":\"auto\",\"bottom_margin\":\"auto\",\"value_bounds\":[null,null],\"y_axis_format\":\"SMART_NUMBER\",\"x_axis_time_format\":\"smart_date\",\"show_legend\":true,\"show_percentage\":true,\"show_values\":true,\"extra_form_data\":{},\"dashboards\":[],\"annotation_layers\":[]}"
}
```

> ⚠️ **IMPORTANTE per v6:**
> - Usare `viz_type`: "heatmap_v2"
> - Il parametro `groupby` deve essere una stringa singola (non array)
> - Il campo `params` deve essere una stringa JSON

---

### 7. **Tree Chart** - Grafico ad Albero


**Endpoint:** `POST /api/v1/chart/`

**Parametri indispensabili:**
- `datasource_id`: ID numerico del dataset (**obbligatorio**)
- `datasource_type`: "table" (**obbligatorio**)
- `slice_name`: Nome del chart (**obbligatorio**)
- `viz_type`: "tree_chart" (**obbligatorio**)
- `params`: Stringa JSON con configurazione (**obbligatorio**)

**Parametri chiave in params:**
- `id`: Colonna ID dei nodi (es. "id") (**obbligatorio**)
- `parent`: Colonna ID del nodo padre (es. "parent") (**obbligatorio**)
- `name`: Colonna nome del nodo (es. "name") (**obbligatorio**)
- `root_node_id`: ID del nodo radice (es. "1") (**obbligatorio**)
- `metric`: Metrica per dimensione nodi (es. "count") (**obbligatorio**)

**Parametri opzionali (default disponibili):**
- `layout`: Tipo layout (default: "radial")
- `node_label_position`: Posizione etichetta nodo (default: "top")
- `child_label_position`: Posizione etichetta figli (default: "top")
- `symbol`: Simbolo nodi (default: "emptyCircle")
- `symbolSize`: Dimensione simboli (default: 7)
- `roam`: Navigazione interattiva (default: false)
- `row_limit`: Limite righe (default: 1000)

**Esempio validato (FUNZIONANTE):**
```json
{
  "datasource_id": 20,
  "datasource_type": "table",
  "slice_name": "Tree Chart Example",
  "viz_type": "tree_chart",
  "params": "{\"datasource\":{\"id\":20,\"type\":\"table\"},\"viz_type\":\"tree_chart\",\"id\":\"id\",\"parent\":\"parent\",\"name\":\"name\",\"root_node_id\":\"1\",\"metric\":\"count\",\"adhoc_filters\":[],\"row_limit\":1000,\"layout\":\"radial\",\"node_label_position\":\"top\",\"child_label_position\":\"top\",\"symbol\":\"emptyCircle\",\"symbolSize\":7,\"roam\":false,\"extra_form_data\":{},\"dashboards\":[],\"annotation_layers\":[]}"
}
```

> ⚠️ **IMPORTANTE per v6:**
> - Usare `viz_type`: "tree_chart" (non "treemap")
> - Richiede dataset con struttura gerarchica (id, parent, name)
> - Il campo `params` deve essere una stringa JSON

---

### 8. **Scatter Plot** - Grafico a Dispersione

> 🔄 **Mappatura UI → API Parameters (echarts_timeseries_scatter):**
> 
**Endpoint:** `POST /api/v1/chart/`

**Parametri indispensabili:**
- `datasource_id`: ID numerico del dataset (**obbligatorio**)
- `datasource_type`: "table" (**obbligatorio**)
- `slice_name`: Nome del chart (**obbligatorio**)
- `viz_type`: "echarts_timeseries_scatter" (**obbligatorio**)
- `params`: Stringa JSON con configurazione (**obbligatorio**)

**Parametri chiave in params:**
- `x_axis`: Colonna asse X (es. "order_date") (**obbligatorio**)
- `metrics`: Metriche per asse Y (es. ["count"]) (**obbligatorio**)
- `groupby`: Raggrupamenti per serie (es. ["deal_size"])

**Parametri opzionali (default disponibili):**
- `time_grain_sqla`: Granularità temporale (default: "P1D")
- `markerSize`: Dimensione marcatori (default: 6)
- `color_scheme`: Schema colori (default: "supersetColors")
- `show_legend`: Mostra legenda (default: true)
- `rich_tooltip`: Tooltip dettagliato (default: true)
- `row_limit`: Limite righe (default: 10000)

**Esempio validato (FUNZIONANTE):**
```json
{
  "datasource_id": 9,
  "datasource_type": "table",
  "slice_name": "Scatter Plot Example",
  "viz_type": "echarts_timeseries_scatter",
  "params": "{\"datasource\":{\"id\":9,\"type\":\"table\"},\"viz_type\":\"echarts_timeseries_scatter\",\"x_axis\":\"order_date\",\"time_grain_sqla\":\"P1D\",\"x_axis_sort_asc\":true,\"x_axis_sort_series\":\"name\",\"x_axis_sort_series_ascending\":true,\"metrics\":[\"count\"],\"groupby\":[\"deal_size\"],\"adhoc_filters\":[{\"clause\":\"WHERE\",\"subject\":\"order_date\",\"operator\":\"TEMPORAL_RANGE\",\"comparator\":\"No filter\",\"expressionType\":\"SIMPLE\"}],\"order_desc\":true,\"row_limit\":10000,\"truncate_metric\":true,\"show_empty_columns\":true,\"comparison_type\":\"values\",\"annotation_layers\":[],\"forecastPeriods\":10,\"forecastInterval\":0.8,\"x_axis_title_margin\":15,\"y_axis_title_margin\":15,\"y_axis_title_position\":\"Left\",\"sort_series_type\":\"sum\",\"color_scheme\":\"supersetColors\",\"only_total\":true,\"markerSize\":6,\"show_legend\":true,\"legendType\":\"scroll\",\"legendOrientation\":\"top\",\"x_axis_time_format\":\"smart_date\",\"rich_tooltip\":true,\"tooltipTimeFormat\":\"smart_date\",\"y_axis_format\":\"SMART_NUMBER\",\"truncateXAxis\":true,\"y_axis_bounds\":[null,null],\"extra_form_data\":{},\"dashboards\":[]}"
}
```

> ⚠️ **IMPORTANTE per v6:**
> - Usare `viz_type`: "echarts_timeseries_scatter" (non "bubble")
> - Simile al bar chart ma con marcatori scatter
> - Il campo `params` deve essere una stringa JSON

---

### 9. **Big Number** - Numero Grande

**Endpoint:** `POST /api/v1/chart/`

**Parametri indispensabili:**
- `datasource_id`: ID numerico del dataset (**obbligatorio**)
- `datasource_type`: "table" (**obbligatorio**)
- `slice_name`: Nome del chart (**obbligatorio**)
- `viz_type`: "big_number_total" (**obbligatorio**)
- `params`: Stringa JSON con configurazione (**obbligatorio**)

**Parametri chiave in params:**
- `metric`: Metrica principale da visualizzare (es. "count") (**obbligatorio**)

**Parametri opzionali (default disponibili):**
- `header_font_size`: Dimensione font titolo (default: 0.4)
- `subheader_font_size`: Dimensione font sottotitolo (default: 0.15)
- `y_axis_format`: Formato del numero (default: "SMART_NUMBER")
- `time_format`: Formato tempo (default: "smart_date")
- `adhoc_filters`: Filtri aggiuntivi (default: [])

**Esempio validato (FUNZIONANTE):**
```json
{
  "datasource_id": 9,
  "datasource_type": "table",
  "slice_name": "Big Number Example",
  "viz_type": "big_number_total",
  "params": "{\"datasource\":{\"id\":9,\"type\":\"table\"},\"viz_type\":\"big_number_total\",\"metric\":\"count\",\"adhoc_filters\":[{\"clause\":\"WHERE\",\"subject\":\"order_date\",\"operator\":\"TEMPORAL_RANGE\",\"comparator\":\"No filter\",\"expressionType\":\"SIMPLE\"}],\"header_font_size\":0.4,\"subheader_font_size\":0.15,\"y_axis_format\":\"SMART_NUMBER\",\"time_format\":\"smart_date\",\"extra_form_data\":{},\"dashboards\":[],\"annotation_layers\":[]}"
}
```

> ⚠️ **IMPORTANTE per v6:**
> - Usare `viz_type`: "big_number_total"
> - Visualizza un singolo valore numerico grande
> - Il campo `params` deve essere una stringa JSON

**API d'esempio (big_number_total):**
```json
{
  "slice_name": "Big Number Example",
  "viz_type": "big_number_total",
  "datasource_id": 1,
  "datasource_type": "table",
  "params": {
    "datasource": "1__table",
    "viz_type": "big_number_total",
    "metric": "count",
    "groupby": "Provincia",
    "time_grain_sqla": "P1D",
    "adhoc_filters": [],
    "row_limit": 10000,
    "y_axis_format": "SMART_NUMBER",
    "show_legend": true,
    "extra_form_data": {},
    "dashboards": []
  },
  "query_context": null
}
```



## 📊 Creazione Dashboard con Filtri tramite API

### Panoramica e Parametri Obbligatori

Questa sezione descrive il workflow e i parametri necessari per creare una dashboard in Superset tramite chiamate API REST, includendo uno o più grafici già esistenti e la configurazione di filtri nativi (native filters).

**Parametri obbligatori:**
- **dashboard_title**: Titolo della dashboard da creare.
- **chart_ids**: Lista degli ID dei grafici (charts) già esistenti da includere nella dashboard.
- **native_filters**: Lista di oggetti che definiscono i filtri nativi da applicare alla dashboard (vedi esempio sotto).

---

### Workflow delle chiamate API per la creazione di dashboard

A differenza della creazione di una chart, la creazione di una dashboard in Superset tramite API **richiede un workflow composto da più chiamate** e la compilazione obbligatoria di alcuni parametri fondamentali. Non è sufficiente una semplice chiamata POST con solo il titolo: per ottenere una dashboard realmente utilizzabile e visualizzare correttamente i grafici, è necessario:

- Specificare **position_json**: struttura che definisce il layout e la posizione dei grafici nella dashboard.
- Specificare **json_metadata**: configurazione avanzata, inclusi i filtri nativi (`native_filter_configuration`).
- Associare esplicitamente i grafici tramite i loro ID.

**Esempio di sequenza chiamate:**

1. **POST** `/security/login` → ottieni token
2. **POST** `/dashboard/`  
   - Parametri: `dashboard_title`, `json_metadata` (con filtri), `position_json` (con chart_ids)
3. **PUT** `/dashboard/{dashboard_id}` (opzionale, per aggiornare posizione grafici)
4. **PUT** `/chart/{chart_id}` (opzionale, per ogni chart, per aggiornare campo dashboards)
5. **GET** `/dashboard/{dashboard_id}` (verifica)

---

### Note tecniche importanti

**⚠️ Struttura position_json obbligatoria**  
Durante la sperimentazione è emerso che senza una corretta configurazione del campo `position_json`, **i grafici non risultano visibili** nella dashboard anche se correttamente associati tramite ID. Una dashboard "vuota" o creata solo con il titolo non è funzionante: la struttura deve contenere obbligatoriamente un blocco ROOT, un blocco GRID, uno o più ROW e i blocchi CHART con i relativi ID e metadati minimi. La struttura `position_json` deve includere tutti i grafici che si desidera visualizzare nella dashboard.
Se non si compila correttamente `position_json` (vedi esempio sotto), i grafici **non saranno visibili** nella dashboard, anche se associati. 

**Altre considerazioni:**
- I **filtri nativi** (`native_filters`) devono essere configurati in base alle colonne e ai dataset effettivamente disponibili
- Gli **ID dei grafici** (`chart_ids`) devono riferirsi a grafici già esistenti, creati tramite API o interfaccia grafica  
- Le chiamate `PUT` per aggiornare posizione e associazione sono **opzionali ma fortemente consigliate** per garantire integrità e visualizzazione corretta

---

## Creazione della Dashboard (Step-by-Step)

### 1. Creazione della dashboard

Effettuare una chiamata `POST` a `/api/v1/dashboard/` per creare la dashboard e associare i grafici e i filtri.

**Body obbligatorio:**
```json
{
  "dashboard_title": "Nome della dashboard",
  "json_metadata": "{...}",
  "published": false,
  "position_json": "{...}"
}
```
- **dashboard_title**: stringa, titolo della dashboard.
- **json_metadata**: stringa JSON che include la configurazione dei filtri nativi (`native_filter_configuration`) e altre opzioni (es: `cross_filters_enabled`, `refresh_frequency`).
- **position_json**: stringa JSON che definisce la struttura della dashboard e la posizione dei grafici (ogni chart deve essere referenziato tramite il suo ID).

---

### 2. Esempi pratici di parametri obbligatori

**1. Esempio di json_metadata (struttura organizzata):**
```json
{
  // === CONFIGURAZIONE FILTRI NATIVI ===
  "native_filter_configuration": [
    // Filtro 1: Tipologia Infrastruttura (applicato a tutti i chart)
    {
      "id": "NATIVE_FILTER-0PMZ2rcO9QpIgYzoz5DQP",
      "name": "Tipologia Infrastruttura",
      "filterType": "filter_select",
      "targets": [
        {
          "column": {"name": "Tipologia di infrastruttura"}, 
          "datasetId": 1
        }
      ],
      "controlValues": {
        "multiSelect": true,           // Consente selezione multipla
        "enableEmptyFilter": false,    // Non consente filtro vuoto
        "defaultToFirstItem": false,   // Non seleziona automaticamente il primo elemento
        "searchAllOptions": false,     // Disabilita ricerca nelle opzioni
        "inverseSelection": false      // Disabilita selezione inversa
      },
      "scope": {
        "rootPath": ["ROOT_ID"], 
        "excluded": []
      },
      "type": "NATIVE_FILTER",
      "chartsInScope": [718, 721, 714, 715],  // Tutti i chart della dashboard
      "tabsInScope": []
    },
    
    // Filtro 2: Provincie (applicato solo al chart 718)
    {
      "id": "NATIVE_FILTER-J_MsNmVvtPHmBMjEA-CVm",
      "name": "Provincie",
      "filterType": "filter_select",
      "targets": [
        {
          "column": {"name": "Provincia"}, 
          "datasetId": 1
        }
      ],
      "controlValues": {
        "multiSelect": true,
        "enableEmptyFilter": false,
        "defaultToFirstItem": false,
        "searchAllOptions": false,
        "inverseSelection": false
      },
      "scope": {
        "rootPath": ["ROOT_ID"], 
        "excluded": []
      },
      "type": "NATIVE_FILTER",
      "chartsInScope": [718],  // Solo il chart 718 (Tabella Costi)
      "tabsInScope": []
    },
    
    // Filtro 3: Zona di fornitura (applicato a tutti i chart)
    {
      "id": "NATIVE_FILTER-IhXqLjq_FDkIzTPIHfacu",
      "name": "ZdF",
      "filterType": "filter_select",
      "targets": [
        {
          "column": {"name": "Zona di fornitura"}, 
          "datasetId": 1
        }
      ],
      "controlValues": {
        "multiSelect": true,
        "enableEmptyFilter": false,
        "defaultToFirstItem": false,
        "searchAllOptions": false,
        "inverseSelection": false
      },
      "scope": {
        "rootPath": ["ROOT_ID"], 
        "excluded": []
      },
      "type": "NATIVE_FILTER",
      "chartsInScope": [718, 721, 714, 715],  // Tutti i chart della dashboard
      "tabsInScope": []
    },
    
    // Filtro 4: Rating R3 (applicato a tutti i chart)
    {
      "id": "NATIVE_FILTER-TAyYFAEJ7HgyGPjNLdlWb",
      "name": "R3",
      "filterType": "filter_select",
      "targets": [
        {
          "column": {"name": "Rating R3 (classe)"}, 
          "datasetId": 1
        }
      ],
      "controlValues": {
        "multiSelect": true,
        "enableEmptyFilter": false,
        "defaultToFirstItem": false,
        "searchAllOptions": false,
        "inverseSelection": false
      },
      "scope": {
        "rootPath": ["ROOT_ID"], 
        "excluded": []
      },
      "type": "NATIVE_FILTER",
      "chartsInScope": [718, 721, 714, 715],  // Tutti i chart della dashboard
      "tabsInScope": []
    }
  ],
  
  // === CONFIGURAZIONE CROSS FILTERS ===
  "cross_filters_enabled": true,        // Abilita filtri incrociati tra chart
  "expanded_slices": {},                 // Chart espansi di default (vuoto = nessuno)
  "refresh_frequency": 0,                // Frequenza auto-refresh in secondi (0 = disabilitato)
  
  // === CONFIGURAZIONE CHART SPECIFICI ===
  "chart_configuration": {
    // Chart 714: Distribuzione Investimenti
    "714": {
      "id": 714,
      "crossFilters": {
        "scope": "global",                           // Scope globale dei cross-filter
        "chartsInScope": [715, 718, 721]            // Chart interessati dai cross-filter di questo chart
      }
    },
    
    // Chart 718: Tabella Costi  
    "718": {
      "id": 718,
      "crossFilters": {
        "scope": "global",
        "chartsInScope": [714, 715, 721]            // Chart interessati dai cross-filter di questo chart
      }
    },
    
    // Chart 721: Pivot Table
    "721": {
      "id": 721,
      "crossFilters": {
        "scope": "global",
        "chartsInScope": [714, 715, 718]            // Chart interessati dai cross-filter di questo chart
      }
    }
  },
  
  // === CONFIGURAZIONE GLOBALE CROSS FILTERS ===
  "global_chart_configuration": {
    "scope": {
      "rootPath": ["ROOT_ID"],           // Path radice per scope globale
      "excluded": []                     // Chart esclusi dai cross-filter globali
    },
    "chartsInScope": [714, 715, 718, 721]  // Tutti i chart inclusi nei cross-filter globali
  }
}
```
> 💡 **Note sui Native Filter ID:**
> - Per una nuova dashboard, **genera un ID univoco** con il pattern `NATIVE_FILTER-{NomeDescrittivo}`



**2. Esempio di position_json:**

> 📋 **Spiegazione della Struttura position_json**
>
> Il `position_json` definisce la struttura gerarchica della dashboard e la posizione di ogni elemento. La struttura è ad albero e segue questo pattern:
>
> **🏗️ Componenti Base:**
> - **ROOT_ID**: Elemento radice che contiene tutto il layout della dashboard
> - **GRID_ID**: Container principale che organizza il contenuto in griglia
> - **ROW-{n}**: Righe che contengono i singoli grafici (layout verticale)
> - **CHART-{n}**: Singoli grafici con i loro metadati e posizionamento
>
> **📊 Questo Esempio Contiene 4 Grafici:**
> 1. **CHART-1** (ID: 718): "Tabella Costi" - Tabella con dati grezzi
> 2. **CHART-2** (ID: 721): "Pivot Table" - Tabella pivot aggregata
> 3. **CHART-3** (ID: 714): "Distribuzione Investimenti" - Grafico di distribuzione
> 4. **CHART-4** (ID: 715): "Media Efficacia" - Metrica di performance
>
> **🎯 Parametri di Posizionamento:**
> - `width`: Larghezza del grafico (4 = occupa 4 colonne della griglia)
> - `height`: Altezza del grafico (50 = 50 unità di altezza)
> - `parents`: Gerarchia di appartenenza (ogni elemento sa a chi appartiene)
> - `children`: Elementi contenuti (ogni container sa cosa contiene)
> - `chartId`/`sliceId`: ID univoco del grafico in Superset
> - `uuid`: Identificatore universale del grafico
> - `sliceName`: Nome visualizzato del grafico

```json
{
  "ROOT_ID": {"type": "ROOT", "id": "ROOT_ID", "children": ["GRID_ID"], "meta": {}, "parents": []},
  "GRID_ID": {"type": "GRID", "id": "GRID_ID", "children": ["ROW-1", "ROW-2", "ROW-3", "ROW-4"], "parents": ["ROOT_ID"]},
  "ROW-1": {"type": "ROW", "id": "ROW-1", "children": ["CHART-1"], "meta": {"background": "BACKGROUND_TRANSPARENT"}, "parents": ["ROOT_ID", "GRID_ID"]},
  "CHART-1": {"type": "CHART", "id": "CHART-1", "children": [], "meta": {"chartId": 718, "sliceId": 718, "slice_id": 718, "uuid": "72118fe1-3446-4199-8ddc-22330b013090", "width": 4, "height": 50, "sliceName": "Tabella Costi"}, "parents": ["ROOT_ID", "GRID_ID", "ROW-1"]},
  "ROW-2": {"type": "ROW", "id": "ROW-2", "children": ["CHART-2"], "meta": {"background": "BACKGROUND_TRANSPARENT"}, "parents": ["ROOT_ID", "GRID_ID"]},
  "CHART-2": {"type": "CHART", "id": "CHART-2", "children": [], "meta": {"chartId": 721, "sliceId": 721, "slice_id": 721, "uuid": "7617144d-cc1b-4bb1-a6b0-706ec1ad3dc6", "width": 4, "height": 50, "sliceName": "Pivot Table"}, "parents": ["ROOT_ID", "GRID_ID", "ROW-2"]},
  "ROW-3": {"type": "ROW", "id": "ROW-3", "children": ["CHART-3"], "meta": {"background": "BACKGROUND_TRANSPARENT"}, "parents": ["ROOT_ID", "GRID_ID"]},
  "CHART-3": {"type": "CHART", "id": "CHART-3", "children": [], "meta": {"chartId": 714, "sliceId": 714, "slice_id": 714, "uuid": "61588bd4-f26a-4f47-a1cc-9b77cd47225a", "width": 4, "height": 50, "sliceName": "Distribuzione Investimenti"}, "parents": ["ROOT_ID", "GRID_ID", "ROW-3"]},
  "ROW-4": {"type": "ROW", "id": "ROW-4", "children": ["CHART-4"], "meta": {"background": "BACKGROUND_TRANSPARENT"}, "parents": ["ROOT_ID", "GRID_ID"]},
  "CHART-4": {"type": "CHART", "id": "CHART-4", "children": [], "meta": {"chartId": 715, "sliceId": 715, "slice_id": 715, "uuid": "18d3613b-4d5b-4dfe-a817-b3dddabab928", "width": 4, "height": 50, "sliceName": "Media Efficacia"}, "parents": ["ROOT_ID", "GRID_ID", "ROW-4"]}
}
```




### 3. Esempio completo di chiamata POST /api/v1/dashboard/

**Endpoint:**  
`POST /api/v1/dashboard/`

**Body completo con i parametri dell'esempio sopra:**

> 📝 **Versione Leggibile (per comprensione):**
```json
{
  "dashboard_title": "Dashboard Infrastrutture Regione Puglia",
  "published": false,
  
  // === JSON_METADATA (struttura espansa per leggibilità) ===
  "json_metadata": {
    "native_filter_configuration": [
      {
        "id": "NATIVE_FILTER-0PMZ2rcO9QpIgYzoz5DQP",
        "name": "Tipologia Infrastruttura",
        "filterType": "filter_select",
        "targets": [{"column": {"name": "Tipologia di infrastruttura"}, "datasetId": 1}],
        "controlValues": {"multiSelect": true, "enableEmptyFilter": false},
        "scope": {"rootPath": ["ROOT_ID"], "excluded": []},
        "type": "NATIVE_FILTER",
        "chartsInScope": [718, 721, 714, 715],
        "tabsInScope": []
      },
      {
        "id": "NATIVE_FILTER-J_MsNmVvtPHmBMjEA-CVm", 
        "name": "Provincie",
        "filterType": "filter_select",
        "targets": [{"column": {"name": "Provincia"}, "datasetId": 1}],
        "controlValues": {"multiSelect": true, "enableEmptyFilter": false},
        "scope": {"rootPath": ["ROOT_ID"], "excluded": []},
        "type": "NATIVE_FILTER",
        "chartsInScope": [718],
        "tabsInScope": []
      },
      {
        "id": "NATIVE_FILTER-IhXqLjq_FDkIzTPIHfacu",
        "name": "ZdF", 
        "filterType": "filter_select",
        "targets": [{"column": {"name": "Zona di fornitura"}, "datasetId": 1}],
        "controlValues": {"multiSelect": true, "enableEmptyFilter": false},
        "scope": {"rootPath": ["ROOT_ID"], "excluded": []},
        "type": "NATIVE_FILTER",
        "chartsInScope": [718, 721, 714, 715],
        "tabsInScope": []
      },
      {
        "id": "NATIVE_FILTER-TAyYFAEJ7HgyGPjNLdlWb",
        "name": "R3",
        "filterType": "filter_select", 
        "targets": [{"column": {"name": "Rating R3 (classe)"}, "datasetId": 1}],
        "controlValues": {"multiSelect": true, "enableEmptyFilter": false},
        "scope": {"rootPath": ["ROOT_ID"], "excluded": []},
        "type": "NATIVE_FILTER",
        "chartsInScope": [718, 721, 714, 715],
        "tabsInScope": []
      }
    ],
    "cross_filters_enabled": true,
    "expanded_slices": {},
    "refresh_frequency": 0,
    "chart_configuration": {
      "714": {"id": 714, "crossFilters": {"scope": "global", "chartsInScope": [715, 718, 721]}},
      "718": {"id": 718, "crossFilters": {"scope": "global", "chartsInScope": [714, 715, 721]}},
      "721": {"id": 721, "crossFilters": {"scope": "global", "chartsInScope": [714, 715, 718]}}
    },
    "global_chart_configuration": {
      "scope": {"rootPath": ["ROOT_ID"], "excluded": []},
      "chartsInScope": [714, 715, 718, 721]
    }
  },
  
  // === POSITION_JSON (struttura espansa per leggibilità) ===
  "position_json": {
    "ROOT_ID": {
      "type": "ROOT",
      "id": "ROOT_ID", 
      "children": ["GRID_ID"],
      "meta": {},
      "parents": []
    },
    "GRID_ID": {
      "type": "GRID",
      "id": "GRID_ID",
      "children": ["ROW-1", "ROW-2", "ROW-3", "ROW-4"],
      "parents": ["ROOT_ID"]
    },
    "ROW-1": {
      "type": "ROW",
      "id": "ROW-1",
      "children": ["CHART-1"],
      "meta": {"background": "BACKGROUND_TRANSPARENT"},
      "parents": ["ROOT_ID", "GRID_ID"]
    },
    "CHART-1": {
      "type": "CHART",
      "id": "CHART-1",
      "children": [],
      "meta": {
        "chartId": 718,
        "sliceId": 718,
        "slice_id": 718,
        "uuid": "72118fe1-3446-4199-8ddc-22330b013090",
        "width": 4,
        "height": 50,
        "sliceName": "Tabella Costi"
      },
      "parents": ["ROOT_ID", "GRID_ID", "ROW-1"]
    },
    "ROW-2": {
      "type": "ROW",
      "id": "ROW-2", 
      "children": ["CHART-2"],
      "meta": {"background": "BACKGROUND_TRANSPARENT"},
      "parents": ["ROOT_ID", "GRID_ID"]
    },
    "CHART-2": {
      "type": "CHART",
      "id": "CHART-2",
      "children": [],
      "meta": {
        "chartId": 721,
        "sliceId": 721,
        "slice_id": 721,
        "uuid": "7617144d-cc1b-4bb1-a6b0-706ec1ad3dc6",
        "width": 4,
        "height": 50,
        "sliceName": "Pivot Table"
      },
      "parents": ["ROOT_ID", "GRID_ID", "ROW-2"]
    },
    "ROW-3": {
      "type": "ROW",
      "id": "ROW-3",
      "children": ["CHART-3"],
      "meta": {"background": "BACKGROUND_TRANSPARENT"},
      "parents": ["ROOT_ID", "GRID_ID"]
    },
    "CHART-3": {
      "type": "CHART",
      "id": "CHART-3",
      "children": [],
      "meta": {
        "chartId": 714,
        "sliceId": 714,
        "slice_id": 714,
        "uuid": "61588bd4-f26a-4f47-a1cc-9b77cd47225a",
        "width": 4,
        "height": 50,
        "sliceName": "Distribuzione Investimenti"
      },
      "parents": ["ROOT_ID", "GRID_ID", "ROW-3"]
    },
    "ROW-4": {
      "type": "ROW",
      "id": "ROW-4",
      "children": ["CHART-4"],
      "meta": {"background": "BACKGROUND_TRANSPARENT"},
      "parents": ["ROOT_ID", "GRID_ID"]
    },
    "CHART-4": {
      "type": "CHART", 
      "id": "CHART-4",
      "children": [],
      "meta": {
        "chartId": 715,
        "sliceId": 715,
        "slice_id": 715,
        "uuid": "18d3613b-4d5b-4dfe-a817-b3dddabab928",
        "width": 4,
        "height": 50,
        "sliceName": "Media Efficacia"
      },
      "parents": ["ROOT_ID", "GRID_ID", "ROW-4"]
    }
  }
}
```

> ⚠️ **Versione API Reale (con stringhe escaped):**
```json
{
  "dashboard_title": "Dashboard Infrastrutture Regione Puglia",
  "published": false,
  "json_metadata": "{\"native_filter_configuration\":[{\"id\":\"NATIVE_FILTER-0PMZ2rcO9QpIgYzoz5DQP\",\"name\":\"Tipologia Infrastruttura\",\"filterType\":\"filter_select\",\"targets\":[{\"column\":{\"name\":\"Tipologia di infrastruttura\"},\"datasetId\":1}],\"controlValues\":{\"multiSelect\":true,\"enableEmptyFilter\":false,\"defaultToFirstItem\":false,\"searchAllOptions\":false,\"inverseSelection\":false},\"scope\":{\"rootPath\":[\"ROOT_ID\"],\"excluded\":[]},\"type\":\"NATIVE_FILTER\",\"chartsInScope\":[718,721,714,715],\"tabsInScope\":[]},{\"id\":\"NATIVE_FILTER-J_MsNmVvtPHmBMjEA-CVm\",\"name\":\"Provincie\",\"filterType\":\"filter_select\",\"targets\":[{\"column\":{\"name\":\"Provincia\"},\"datasetId\":1}],\"controlValues\":{\"multiSelect\":true,\"enableEmptyFilter\":false,\"defaultToFirstItem\":false,\"searchAllOptions\":false,\"inverseSelection\":false},\"scope\":{\"rootPath\":[\"ROOT_ID\"],\"excluded\":[]},\"type\":\"NATIVE_FILTER\",\"chartsInScope\":[718],\"tabsInScope\":[]},{\"id\":\"NATIVE_FILTER-IhXqLjq_FDkIzTPIHfacu\",\"name\":\"ZdF\",\"filterType\":\"filter_select\",\"targets\":[{\"column\":{\"name\":\"Zona di fornitura\"},\"datasetId\":1}],\"controlValues\":{\"multiSelect\":true,\"enableEmptyFilter\":false,\"defaultToFirstItem\":false,\"searchAllOptions\":false,\"inverseSelection\":false},\"scope\":{\"rootPath\":[\"ROOT_ID\"],\"excluded\":[]},\"type\":\"NATIVE_FILTER\",\"chartsInScope\":[718,721,714,715],\"tabsInScope\":[]},{\"id\":\"NATIVE_FILTER-TAyYFAEJ7HgyGPjNLdlWb\",\"name\":\"R3\",\"filterType\":\"filter_select\",\"targets\":[{\"column\":{\"name\":\"Rating R3 (classe)\"},\"datasetId\":1}],\"controlValues\":{\"multiSelect\":true,\"enableEmptyFilter\":false,\"defaultToFirstItem\":false,\"searchAllOptions\":false,\"inverseSelection\":false},\"scope\":{\"rootPath\":[\"ROOT_ID\"],\"excluded\":[]},\"type\":\"NATIVE_FILTER\",\"chartsInScope\":[718,221,714,715],\"tabsInScope\":[]}],\"cross_filters_enabled\":true,\"expanded_slices\":{},\"refresh_frequency\":0,\"chart_configuration\":{\"714\":{\"id\":714,\"crossFilters\":{\"scope\":\"global\",\"chartsInScope\":[715,718,721]}},\"718\":{\"id\":718,\"crossFilters\":{\"scope\":\"global\",\"chartsInScope\":[714,715,721]}},\"721\":{\"id\":721,\"crossFilters\":{\"scope\":\"global\",\"chartsInScope\":[714,715,718]}}},\"global_chart_configuration\":{\"scope\":{\"rootPath\":[\"ROOT_ID\"],\"excluded\":[]},\"chartsInScope\":[714,715,718,721]}}",
  "position_json": "{\"ROOT_ID\":{\"type\":\"ROOT\",\"id\":\"ROOT_ID\",\"children\":[\"GRID_ID\"],\"meta\":{},\"parents\":[]},\"GRID_ID\":{\"type\":\"GRID\",\"id\":\"GRID_ID\",\"children\":[\"ROW-1\",\"ROW-2\",\"ROW-3\",\"ROW-4\"],\"parents\":[\"ROOT_ID\"]},\"ROW-1\":{\"type\":\"ROW\",\"id\":\"ROW-1\",\"children\":[\"CHART-1\"],\"meta\":{\"background\":\"BACKGROUND_TRANSPARENT\"},\"parents\":[\"ROOT_ID\",\"GRID_ID\"]},\"CHART-1\":{\"type\":\"CHART\",\"id\":\"CHART-1\",\"children\":[],\"meta\":{\"chartId\":718,\"sliceId\":718,\"slice_id\":718,\"uuid\":\"72118fe1-3446-4199-8ddc-22330b013090\",\"width\":4,\"height\":50,\"sliceName\":\"Tabella Costi\"},\"parents\":[\"ROOT_ID\",\"GRID_ID\",\"ROW-1\"]},\"ROW-2\":{\"type\":\"ROW\",\"id\":\"ROW-2\",\"children\":[\"CHART-2\"],\"meta\":{\"background\":\"BACKGROUND_TRANSPARENT\"},\"parents\":[\"ROOT_ID\",\"GRID_ID\"]},\"CHART-2\":{\"type\":\"CHART\",\"id\":\"CHART-2\",\"children\":[],\"meta\":{\"chartId\":721,\"sliceId\":721,\"slice_id\":721,\"uuid\":\"7617144d-cc1b-4bb1-a6b0-706ec1ad3dc6\",\"width\":4,\"height\":50,\"sliceName\":\"Pivot Table\"},\"parents\":[\"ROOT_ID\",\"GRID_ID\",\"ROW-2\"]},\"ROW-3\":{\"type\":\"ROW\",\"id\":\"ROW-3\",\"children\":[\"CHART-3\"],\"meta\":{\"background\":\"BACKGROUND_TRANSPARENT\"},\"parents\":[\"ROOT_ID\",\"GRID_ID\"]},\"CHART-3\":{\"type\":\"CHART\",\"id\":\"CHART-3\",\"children\":[],\"meta\":{\"chartId\":714,\"sliceId\":714,\"slice_id\":714,\"uuid\":\"61588bd4-f26a-4f47-a1cc-9b77cd47225a\",\"width\":4,\"height\":50,\"sliceName\":\"Distribuzione Investimenti\"},\"parents\":[\"ROOT_ID\",\"GRID_ID\",\"ROW-3\"]},\"ROW-4\":{\"type\":\"ROW\",\"id\":\"ROW-4\",\"children\":[\"CHART-4\"],\"meta\":{\"background\":\"BACKGROUND_TRANSPARENT\"},\"parents\":[\"ROOT_ID\",\"GRID_ID\"]},\"CHART-4\":{\"type\":\"CHART\",\"id\":\"CHART-4\",\"children\":[],\"meta\":{\"chartId\":715,\"sliceId\":715,\"slice_id\":715,\"uuid\":\"18d3613b-4d5b-4dfe-a817-b3dddabab928\",\"width\":4,\"height\":50,\"sliceName\":\"Media Efficacia\"},\"parents\":[\"ROOT_ID\",\"GRID_ID\",\"ROW-4\"]}}"
}
```

> 💡 **Nota Importante**: I campi `json_metadata` e `position_json` devono essere stringhe JSON "escaped" (con i caratteri " sostituiti da \"), come mostrato nell'esempio sopra. Non passare oggetti JSON direttamente, ma stringhe contenenti JSON.

### 4. (Opzionale) Aggiornamento posizione grafici

Se necessario dopo la creazione, effettuare una chiamata `PUT` a `/dashboard/{dashboard_id}` per aggiornare la struttura `position_json` della dashboard.

**Endpoint:**  
`PUT /api/v1/dashboard/{dashboard_id}`

**Body:**
```json
{
  "position_json": "{\"ROOT_ID\": {...}, ...}" // struttura aggiornata con tutti i chart_ids
}
```

### 5. (Opzionale) Associazione esplicita dei grafici alla dashboard

Per ogni grafico, effettuare una chiamata `PUT` a `/chart/{chart_id}` per aggiornare il campo `dashboards` e assicurare l'integrità referenziale.

**Endpoint:**  
`PUT /api/v1/chart/{chart_id}`

**Body:**
```json
{
  "dashboards": [dashboard_id]
}
```

### 6. Verifica finale

Effettuare una chiamata `GET` a `/dashboard/{dashboard_id}` per verificare che la dashboard sia stata creata correttamente e che i grafici risultino associati e visibili.

---


---
## 🗄️ Creazione Dataset

 _Sezione in costruzione: qui verrà documentato come creare un dataset via API, con esempi e parametri._

---

