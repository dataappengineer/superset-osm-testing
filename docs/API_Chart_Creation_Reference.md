
# 📊 Riferimento API per Creazione Chart Superset

## 🎯 Obiettivo
Documentazione dettagliata dei parametri API e esempi pratici per la creazione automatica di chart e dashboard in Superset tramite chiamate REST.

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

- **API_BASE**: URL base delle API REST di Superset (es: `http://localhost:8088/api/v1`)
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

> 🔄 **Mappatura UI → API Parameters:**
> 
> **Modalità RAW:**
> | **UI Superset** | **API Parameter** | **Descrizione** |
> |-----------------|------------------|-----------------|
> | **Columns** | `all_columns` | Colonne da visualizzare |
> | **Filters** | `adhoc_filters` | Filtri sui dati |
> | **Ordering** | `order_by_cols` | Ordinamento colonne |
> | **Server Pagination** | `server_pagination` | Paginazione server-side |
> 

**Modalità RAW** (per visualizzare record effettivi):

**Parametri indispensabili:**
- `query_mode`: "raw" - Mostra dati non aggregati dal dataset (**obbligatorio**)
- `all_columns`: Array di nomi colonne da visualizzare (**obbligatorio**)

**Parametri opzionali (default disponibili):**
- `adhoc_filters`: Filtri sui dati in formato array (default: nessun filtro)
  - `[{"col": "regione", "op": "==", "val": "Lombardia"}]` = filtra per regione Lombardia
  - `[{"col": "importo", "op": ">", "val": 1000}]` = filtra importi maggiori di 1000
  - `[{"col": "data", "op": ">=", "val": "2025-01-01"}]` = filtra da data specifica
- `order_by_cols`: Ordinamento colonne in formato array (default: nessun ordinamento)
  - `[["colonna1", true]]` = ordina per colonna1 discendente (Z→A, 100→1)
  - `[["colonna1", false]]` = ordina per colonna1 crescente (A→Z, 1→100)
  - `[["col1", true], ["col2", false]]` = ordinamento multiplo
- `server_pagination`: Paginazione server-side (true/false, default: false)
  - `true` = paginazione gestita dal server (per dataset grandi)
  - `false` = tutti i dati caricati in una volta (solo per dataset piccoli)
- `row_limit`: Numero massimo di righe (default: 100)
- `table_timestamp_format`: Formato timestamp (default: "smart_date")
  - `"smart_date"` = formato intelligente (es. "2 ore fa", "ieri")
  - `"yyyy-MM-dd"` = formato data (es. "2025-09-29")
  - `"yyyy-MM-dd HH:mm:ss"` = formato completo con ora


**API d'esempio (RAW mode) - versione minima e commentata**:
```jsonc
// Esempio di chiamata POST /api/v1/chart/ per una tabella RAW
// - params: definisce la configurazione della visualizzazione (come la vedi in Superset)
// - query_context: definisce la query SQL sottostante (colonne, metriche, limiti, ecc)
// - Alcuni parametri (es. datasource, colonne) sono ripetuti per separare logica di query e visualizzazione
// - "datasource": "1__table" è la forma raccomandata: ID numerico + tipo (non il nome del dataset!)
// - Puoi omettere campi come granularity_sqla, time_range, url_params se non servono
// - groupby e metrics possono essere lasciati vuoti in modalità RAW
{
  "slice_name": "Tabella Dataset - Dati Raw",
  "viz_type": "table",
  "datasource_id": 1,
  "datasource_type": "table",
  "params": {
    "datasource": "1__table", // ID e tipo del dataset (NON il nome!)
    "viz_type": "table",
    "query_mode": "raw",
    "all_columns": ["column1", "column2", "column3"],
    "adhoc_filters": [
      {"col": "column1", "op": "!=", "val": null}
    ],
    "order_by_cols": [["column1", true]],
    "server_pagination": true,
    "order_desc": true,
    "show_totals": false,
    "table_timestamp_format": "smart_date",
    "row_limit": 100
  },
  "query_context": {
    "datasource": {"id": 1, "type": "table"},
    "queries": [{
      "columns": ["column1", "column2", "column3"],
      "metrics": [],
      "row_limit": 100
    }]
  }
}
```

 NOTA su "datasource":
- "datasource": "1__table" significa: usa il dataset con ID 1 e tipo "table".
 - NON usare il nome del dataset (es. "table_1") in questo campo: è meno robusto e può causare errori.
 - L'ID numerico è sempre preferibile e universale.
--------

> **Modalità AGGREGATE:**
> | **UI Superset** | **API Parameter** | **Descrizione** |
> |-----------------|------------------|-----------------|
> | **Dimensions** | `groupby` | Colonne per raggruppamento |
> | **Metrics** | `metrics` | Metriche da calcolare |
> | **Percentage Metrics** | `percent_metrics` | Metriche percentuali |
> | **Filters** | `adhoc_filters` | Filtri sui dati |
> | **Sort by** | `order_by_cols` | Ordinamento colonne |
> | **Row limit** | `row_limit` | Limite righe |

**Modalità AGGREGATE** (per metriche aggregate):

**Parametri indispensabili:**
- `query_mode`: "aggregate" - Raggruppa e aggrega dati (**obbligatorio**)
- `groupby`: Colonne per raggruppamento (es. ["regione", "categoria"]) (**obbligatorio**)
- `metrics` **oppure** `adhoc_metrics`: Metriche aggregate definite nel dataset o create al volo (**almeno una obbligatoria**)

**Parametri opzionali (default disponibili):**
- `percent_metrics`: Metriche percentuali in formato array (default: nessuna)
  - `["sum__importo"]` = mostra percentuale della metrica rispetto al totale
  - `["count", "sum__vendite"]` = multiple metriche percentuali
  - Le percentuali sono calcolate rispetto al totale complessivo
- `adhoc_filters`: Filtri sui dati in formato array (default: nessun filtro)
  - `[{"col": "regione", "op": "==", "val": "Lombardia"}]` = filtra per regione specifica
  - `[{"col": "importo", "op": ">", "val": 1000}]` = filtra valori numerici
  - `[{"col": "data", "op": ">=", "val": "2025-01-01"}]` = filtra date
- `order_by_cols`: Ordinamento colonne in formato array (default: nessun ordinamento)
  - `[["sum__importo", true]]` = ordina per metrica discendente
  - `[["regione", false]]` = ordina per dimensione crescente
  - `[["metric1", true], ["dimension1", false]]` = ordinamento multiplo
- `row_limit`: Numero massimo di righe aggregate da restituire (default: 100)

⚠️ **IMPORTANTE:**
La chiave `metrics` si riferisce alle metriche predefinite già presenti nel dataset Superset (di default è disponibile solo `count`).
Ecco delgi esempi: 
> - `"count"` = conteggio record (sempre disponibile)
> - `"sum__importo"` = somma della colonna "importo" (se definita nel dataset)
> - `"avg__prezzo"` = media della colonna "prezzo" (se definita nel dataset)
> - `"max__data"` = massimo della colonna "data" (se definita nel dataset)
> 
> Usa `GET /api/v1/dataset/{id}` per vedere le metriche disponibili!
>
> 💡 **ALTERNATIVA: Metriche Adhoc (definite al volo tramite API)**
> 
> Se non hai metriche predefinite, puoi crearle direttamente "on the fly" nella richiesta usando `adhoc_metrics`:

> 
> ```json
> "adhoc_metrics": [
>   {
>     "expressionType": "SIMPLE",
>     "column": {"column_name": "importo", "type": "DOUBLE"},
>     "aggregate": "SUM",
>     "label": "Totale Vendite"
>   },
>   {
>     "expressionType": "SIMPLE", 
>     "column": {"column_name": "prezzo", "type": "DOUBLE"},
>     "aggregate": "AVG",
>     "label": "Prezzo Medio"
>   },
>   {
>     "expressionType": "SQL",
>     "sqlExpression": "COUNT(DISTINCT customer_id)",
>     "label": "Clienti Unici"
>   }
> ]
> ```
> 
> **Tipi di aggregazione supportati:**
> - `SUM`, `AVG`, `COUNT`, `COUNT_DISTINCT`, `MIN`, `MAX`
> - `expressionType: "SIMPLE"` = aggregazione standard su colonna
> - `expressionType: "SQL"` = espressione SQL personalizzata



**API d'esempio (AGGREGATE mode)**:
```json
{
  "slice_name": "Tabella Vendite per Regione",
  "viz_type": "table", 
  "datasource_id": 1,
  "datasource_type": "table",
  "params": {
    "datasource": "1__table",
    "viz_type": "table",
    "slice_id": null,
    "url_params": {},
    "granularity_sqla": null,
    "time_range": "No filter",
    "query_mode": "aggregate",
    "groupby": ["regione"],
    "metrics": [],
    "adhoc_metrics": [
      {
        "expressionType": "SIMPLE",
        "column": {"column_name": "importo", "type": "DOUBLE"},
        "aggregate": "SUM",
        "label": "Totale Vendite"
      }
    ],
    "all_columns": [],
    "percent_metrics": [],
    "adhoc_filters": [
      {"col": "regione", "op": "!=", "val": null}
    ],
    "order_by_cols": [["Totale Vendite", true]],
    "order_desc": true,
    "show_totals": false,
    "table_timestamp_format": "smart_date",
    "page_length": 0,
    "include_search": false,
    "show_cell_bars": true,
    "row_limit": 100,
    "extra_form_data": {}
  },
  "query_context": {
    "datasource": {"id": 1, "type": "table"},
    "queries": [{
      "columns": ["regione"],
      "metrics": [
        {
          "expressionType": "SIMPLE",
          "column": {"column_name": "importo", "type": "DOUBLE"},
          "aggregate": "SUM",
          "label": "Totale Vendite"
        }
      ],
      "row_limit": 100
    }]
  }
```
----

### 2. **Pivot Table** - Tabella Pivot

> 🔄 **Mappatura UI → API Parameters:**
> 
> | **UI Superset** | **API Parameter (legacy)** | **API Parameter (pivot_table_v2)** | **Descrizione** |
> |-----------------|---------------------------|-------------------------------|-----------------|
> | **Rows**        | `groupby`                 | `groupbyColumns`               | Righe della pivot |
> | **Columns**     | `columns`                 | `groupbyRows`                   | Colonne della pivot |
> | **Metrics**     | `metrics`                 | `metrics`                       | Valori da aggregare |
> | **Aggregation** | `pandas_aggfunc`          | `aggregateFunction`             | Funzione di aggregazione |
> | **Show totals** | `pivot_margins`           | (non usato, v2 mostra sempre)   | Mostra totali marginali |


**Parametri indispensabili (pivot_table_v2):**
- `groupbyColumns`: Righe della pivot (es. ["Provincia"])
- `groupbyRows`: Colonne della pivot (es. ["Comune"])
- `metrics`: Nomi delle metriche già definite nel dataset

**Parametri opzionali (pivot_table_v2):**
- `aggregateFunction`: Funzione di aggregazione (default: "Sum")
- `metricsLayout`: Disposizione metriche (default: "ROWS")
- `row_limit`: Limite righe (default: 10000)
- `order_desc`: Ordinamento discendente (default: true)
- `valueFormat`: Formato valori (default: "SMART_NUMBER")
- `date_format`: Formato data (default: "smart_date")
- `rowOrder`, `colOrder`: Ordinamento righe/colonne (default: "key_a_to_z")

> 📊 **Esempio Pivot con `pivot_table_v2` :**
> ```json
> {
>   "datasource": "1__table",
>   "viz_type": "pivot_table_v2",
>   "groupbyColumns": ["Provincia"],
>   "groupbyRows": ["Comune"],
>   "time_grain_sqla": "P1D",
>   "temporal_columns_lookup": {},
>   "metrics": ["count"],
>   "metricsLayout": "ROWS",
>   "adhoc_filters": [],
>   "row_limit": 10000,
>   "order_desc": true,
>   "aggregateFunction": "Sum",
>   "valueFormat": "SMART_NUMBER",
>   "date_format": "smart_date",
>   "rowOrder": "key_a_to_z",
>   "colOrder": "key_a_to_z",
>   "extra_form_data": {},
>   "dashboards": []
> }
> ```


### 3. **Bar Chart** - Grafico a Barre

> 🔄 **Mappatura UI → API Parameters:**
> 
> | **UI Superset** | **API Parameter** | **Descrizione** |
> |-----------------|------------------|-----------------|
> | **Dimensions** | `groupby` | Categorie per asse X |
> | **Metrics** | `metrics` | Valori per asse Y |
> | **Series limit** | `series_limit` | Limite numero serie |
> | **Row limit** | `row_limit` | Limite righe dataset |
> | **Color Scheme** | `color_scheme` | Schema colori |
> | **Show Legend** | `show_legend` | Mostra legenda |

**Parametri specifici**:

**Parametri indispensabili:**
- `groupby`: Colonne da usare per l'asse X (es. ["regione"]) (**obbligatorio**)
- `metrics`: Metriche da visualizzare sull'asse Y (es. ["sum__importo"]) (**almeno una obbligatoria**)

**Parametri opzionali (default disponibili):**
- `x_axis_label`: Solo etichetta testuale dell'asse X (default: nessuna)
- `y_axis_label`: Solo etichetta testuale dell'asse Y (default: nessuna)
- `color_scheme`: Schema colori (default: "bnbColors")
- `show_legend`: Mostra legenda (true/false, default: true)
- `rich_tooltip`: Tooltip dettagliato con più informazioni (true/false, default: false)
- `bottom_margin`: Margine inferiore (default: "auto")
- `x_ticks_layout`: Layout etichette asse X (default: "auto")


**API d'esempio**:
```json
{
  "slice_name": "Vendite per Regione - Bar Chart",
  "viz_type": "dist_bar",
  "datasource_id": 15,
  "datasource_type": "table",
  "params": {
    "groupby": ["regione"],
    "metrics": ["sum__importo"],
    "color_scheme": "bnbColors",
    "show_legend": true,
    "rich_tooltip": true,
    "x_axis_label": "Regione",
    "y_axis_label": "Importo Vendite (€)",
    "bottom_margin": "auto",
    "x_ticks_layout": "auto"
  },
  "query_context": {
    "datasource": {"id": 15, "type": "table"},
    "queries": [{
      "columns": ["regione"],
      "metrics": ["sum__importo"],
      "row_limit": 50,
      "orderby": [["sum__importo", false]]
    }]
  }
}
```

### 4. **Pie Chart** - Grafico a Torta

> 🔄 **Mappatura UI → API Parameters:**
> 
> | **UI Superset** | **API Parameter** | **Descrizione** |
> |-----------------|------------------|-----------------|
> | **Dimensions** | `groupby` | Categorie per spicchi |
> | **Metric** | `metric` | Valore per dimensioni |
> | **Donut** | `donut` | Stile ciambella |
> | **Show Labels** | `show_labels` | Mostra etichette |
> | **Labels Outside** | `labels_outside` | Etichette esterne |
> | **Outer Radius** | `outerRadius` | Raggio esterno |
> | **Inner Radius** | `innerRadius` | Raggio interno |

**Parametri specifici**:

**Parametri indispensabili:**
- `groupby`: Colonne da raggruppare (es. ["categoria_prodotto", "regione"]) (**obbligatorio**)
- `metric`: Metrica singola per dimensioni spicchi (es. "sum__importo") (**obbligatorio**)

**Parametri opzionali (default disponibili):**
- `donut`: Stile ciambella con buco centrale (true/false, default: false)
- `show_labels`: Mostra etichette sui spicchi (true/false, default: true)
- `labels_outside`: Etichette fuori dal grafico (true/false, default: false)
- `color_scheme`: Schema colori (default: "bnbColors")
- `outerRadius`: Raggio esterno in % (default: 70)
- `innerRadius`: Raggio interno per donut in % (default: 30)
- `number_format`: Formato numeri (default: ",.0f")

**API d'esempio**:
```json
{
  "slice_name": "Distribuzione Vendite per Categoria - Pie Chart",
  "viz_type": "pie",
  "datasource_id": 15,
  "datasource_type": "table",
  "params": {
    "groupby": ["categoria_prodotto"],
    "metric": "sum__importo",
    "donut": false,
    "show_labels": true,
    "labels_outside": true,
    "color_scheme": "google",
    "outerRadius": 70,
    "innerRadius": 30,
    "number_format": ",.0f"
  },
  "query_context": {
    "datasource": {"id": 15, "type": "table"},
    "queries": [{
      "columns": ["categoria_prodotto"],
      "metrics": ["sum__importo"],
      "row_limit": 20
    }]
  }
}
```

### 5. **Line Chart** - Grafico a Linee

> 🔄 **Mappatura UI → API Parameters:**
> 
> | **UI Superset** | **API Parameter** | **Descrizione** |
> |-----------------|------------------|-----------------|
> | **X-axis** | `granularity_sqla` | Colonna temporale |
> | **Time Range** | `time_range` | Range temporale |
> | **Time Grain** | `time_grain_sqla` | Granularità tempo |
> | **Metrics** | `metrics` | Metriche asse Y |
> | **Dimensions** | `groupby` | Serie multiple |
> | **Contribution** | `contribution` | Modalità contribuzione |
> | **Series limit** | `series_limit` | Limite numero serie |
> | **Row limit** | `row_limit` | Limite righe dataset |

**Parametri specifici**:

**Parametri indispensabili:**
- `granularity_sqla`: Colonna temporale per X-axis (es. "data_vendita") (**obbligatorio**)
- `metrics`: Metriche per asse Y (es. ["sum__importo"]) (**almeno una obbligatoria**)

**Parametri opzionali (default disponibili):**
- `time_range`: Range temporale (default: "No filter")
- `time_grain_sqla`: Granularità tempo (default: nessuna)
- `groupby`: Dimensions - linee multiple per categoria (default: nessuna)
- `contribution`: Contribution mode (true/false, default: false)
- `series_limit`: Series limit (default: nessun limite)
- `line_interpolation`: Tipo interpolazione (default: "linear")
- `show_markers`: Mostra punti sui dati (default: false)
- `y_axis_format`: Formato asse Y (default: ",.0f")
- `color_scheme`: Schema colori (default: "bnbColors")
- `row_limit`: Row limit (default: 1000)

**API d'esempio**:
```json
{
  "slice_name": "Trend Vendite nel Tempo - Line Chart",
  "viz_type": "line",
  "datasource_id": 15,
  "datasource_type": "table",
  "params": {
    "granularity_sqla": "data_vendita",
    "time_grain_sqla": "P1M",
    "time_range": "Last year",
    "metrics": ["sum__importo"],
    "groupby": ["categoria_prodotto"],
    "line_interpolation": "linear",
    "show_markers": true,
    "y_axis_format": ",.0f",
    "color_scheme": "bnbColors"
  },
  "query_context": {
    "datasource": {"id": 15, "type": "table"},
    "queries": [{
      "columns": ["categoria_prodotto"],
      "metrics": ["sum__importo"],
      "granularity": "data_vendita",
      "time_range": "Last year",
      "extras": {
        "time_grain_sqla": "P1M"
      }
    }]
  }
}
```

### 6. **Heat Map** - Mappa di Calore

> 🔄 **Mappatura UI → API Parameters (heatmap_v2):**
> 
> | **UI Superset** | **API Parameter** | **Descrizione** |
> |-----------------|------------------|-----------------|
> | **X Axis**      | `x_axis`         | Colonna asse X |
> | **Y Axis**      | `groupby`        | Colonna asse Y |
> | **Metric**      | `metric`         | Metrica per intensità |
> | **Normalize**   | `normalize_across` | Tipo normalizzazione |
> | **X Scale Interval** | `xscale_interval` | Intervallo scala X |
> | **Y Scale Interval** | `yscale_interval` | Intervallo scala Y |
> | **Color Scheme**| `linear_color_scheme` | Gradiente colori |
> | **Legend**      | `legend_type`    | Tipo legenda |
> | **Show %**      | `show_percentage`| Mostra percentuali |
> | **Row Limit**   | `row_limit`      | Limite righe |

**Parametri indispensabili:**
- `x_axis`: Colonna asse X (es. "Latitudine") (**obbligatorio**)
- `groupby`: Colonna asse Y (es. "Longitudine") (**obbligatorio**)
- `metric`: Metrica per intensità colore (es. "sum__importo") (**obbligatorio**)

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
- `row_limit`: Limite righe (default: 10000)

**API d'esempio (heatmap_v2):**
```json
{
  "slice_name": "Heatmap Latitudine vs Longitudine",
  "viz_type": "heatmap_v2",
  "datasource_id": 1,
  "datasource_type": "table",
  "params": {
    "datasource": "1__table",
    "viz_type": "heatmap_v2",
    "x_axis": "Latitudine",
    "groupby": "Longitudine",
    "metric": "count",
    "time_grain_sqla": "P1D",
    "adhoc_filters": [],
    "row_limit": 10000,
    "sort_x_axis": "alpha_asc",
    "sort_y_axis": "alpha_asc",
    "normalize_across": "heatmap",
    "legend_type": "continuous",
    "linear_color_scheme": "superset_seq_1",
    "xscale_interval": -1,
    "yscale_interval": -1,
    "left_margin": "auto",
    "bottom_margin": "auto",
    "value_bounds": [null, null],
    "y_axis_format": "SMART_NUMBER",
    "x_axis_time_format": "smart_date",
    "show_legend": true,
    "show_percentage": true,
    "extra_form_data": {},
    "dashboards": []
  },
  "query_context": null
}
```

### 7. **Tree Chart** - Grafico ad Albero

> 🔄 **Mappatura UI → API Parameters:**
> 
> | **UI Superset** | **API Parameter** | **Descrizione** |
> |-----------------|------------------|-----------------|
> | **Hierarchy** | `groupby` | Gerarchia categorie |
> | **Metric** | `metric` | Metrica per dimensioni |
> | **Treemap Ratio** | `treemap_ratio` | Rapporto geometrico |
> | **Number Format** | `number_format` | Formato numeri |
> | **Color Scheme** | `color_scheme` | Schema colori |

**Parametri specifici**:

**Parametri indispensabili:**
- `groupby`: Gerarchia delle categorie (es. ["categoria_prodotto", "sottocategoria"]) (**obbligatorio**)
- `metric`: Metrica per dimensione nodi (es. "sum__importo") (**obbligatorio**)

**Parametri opzionali (default disponibili):**
- `treemap_ratio`: Rapporto geometrico (default: 1.618)
- `number_format`: Formato numeri (default: ",.0f")
- `color_scheme`: Schema colori (default: "bnbColors")

**API d'esempio**:
```json
{
  "slice_name": "Tree Chart Vendite per Categoria e Sottocategoria",
  "viz_type": "treemap",
  "datasource_id": 15,
  "datasource_type": "table",
  "params": {
    "groupby": ["categoria_prodotto", "sottocategoria"],
    "metric": "sum__importo",
    "treemap_ratio": 1.618,
    "number_format": ",.0f",
    "color_scheme": "bnbColors"
  },
  "query_context": {
    "datasource": {"id": 15, "type": "table"},
    "queries": [{
      "columns": ["categoria_prodotto", "sottocategoria"],
      "metrics": ["sum__importo"],
      "row_limit": 100
    }]
  }
}
```

### 8. **Scatter Plot** - Grafico a Dispersione

> 🔄 **Mappatura UI → API Parameters:**
> 
> | **UI Superset** | **API Parameter** | **Descrizione** |
> |-----------------|------------------|-----------------|
> | **X Axis** | `x` | Metrica asse X |
> | **Y Axis** | `y` | Metrica asse Y |
> | **Bubble Size** | `size` | Metrica per dimensione |
> | **Series** | `entity` | Colonna per entità |
> | **Max Bubble Size** | `max_bubble_size` | Dimensione massima |
> | **X Log Scale** | `x_log_scale` | Scala logaritmica X |
> | **Y Log Scale** | `y_log_scale` | Scala logaritmica Y |

**Parametri specifici**:

**Parametri indispensabili:**
- `x`: Metrica asse X (es. "sum__importo") (**obbligatorio**)
- `y`: Metrica asse Y (es. "avg__margine") (**obbligatorio**)
- `entity`: Colonna per entità/etichette (es. "regione") (**obbligatorio**)

**Parametri opzionali (default disponibili):**
- `size`: Metrica per dimensione punti (default: "count")
- `max_bubble_size`: Dimensione massima bolle in % (default: "25")
- `color_scheme`: Schema colori (default: "bnbColors")
- `show_legend`: Mostra legenda (default: true)
- `x_axis_label`: Etichetta asse X (default: nessuna)
- `y_axis_label`: Etichetta asse Y (default: nessuna)
- `x_log_scale`: Scala logaritmica asse X (default: false)
- `y_log_scale`: Scala logaritmica asse Y (default: false)

**API d'esempio**:
```json
{
  "slice_name": "Scatter Plot Vendite vs Margini",
  "viz_type": "bubble",
  "datasource_id": 15,
  "datasource_type": "table",
  "params": {
    "x": "sum__importo",
    "y": "avg__margine",
    "size": "count",
    "entity": "regione",
    "max_bubble_size": "25",
    "color_scheme": "bnbColors",
    "show_legend": true,
    "x_axis_label": "Vendite Totali",
    "y_axis_label": "Margine Medio",
    "x_log_scale": false,
    "y_log_scale": false
  },
  "query_context": {
    "datasource": {"id": 15, "type": "table"},
    "queries": [{
      "columns": ["regione"],
      "metrics": ["sum__importo", "avg__margine", "count"],
      "row_limit": 100
    }]
  }
}
```

### 9. **Big Number** - Numero Grande

> 🔄 **Mappatura UI → API Parameters (big_number_total):**
> 
> | **UI Superset** | **API Parameter** | **Descrizione** |
> |-----------------|------------------|-----------------|
> | **Metric**      | `metric`         | Metrica principale |
> | **Y Axis**      | `groupby`        | Raggruppamento opzionale |
> | **Time Grain**  | `time_grain_sqla`| Granularità temporale |
> | **Row Limit**   | `row_limit`      | Limite righe |
> | **Y Axis Format** | `y_axis_format` | Formato numero |
> | **Show Legend** | `show_legend`    | Mostra legenda |
> | **Extra**       | ...              | Altri parametri |

**Parametri indispensabili:**
- `metric`: Metrica principale da visualizzare (es. "count") (**obbligatorio**)

**Parametri opzionali (default disponibili):**
- `groupby`: Raggruppamento opzionale (default: nessuno)
- `time_grain_sqla`: Granularità temporale (default: "P1D")
- `row_limit`: Limite righe (default: 10000)
- `y_axis_format`: Formato del numero (default: "SMART_NUMBER")
- `show_legend`: Mostra legenda (default: true)
- `extra_form_data`, `dashboards`: Parametri aggiuntivi

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


## 🔧 Schema Base della Richiesta POST /api/v1/chart/

Tutti i chart condividono una struttura base comune:

```json
{
  "slice_name": "Nome del Chart",           // Titolo visualizzato
  "viz_type": "table",                      // Tipo di visualizzazione
  "datasource_id": 15,                      // ID del dataset
  "datasource_type": "table",               // Sempre "table" per dataset
  "params": {                               // Configurazione specifica del chart
    // Parametri specifici per ogni tipo di chart
  },
  "query_context": {                        // Contesto della query
    "datasource": {
      "id": 15,
      "type": "table"
    },
    "force": false,
    "queries": [
      {
        "columns": [],                      // Colonne selezionate
        "metrics": [],                      // Metriche calcolate
        "filters": [],                      // Filtri applicati
        "orderby": [],                      // Ordinamento
        "annotation_layers": [],
        "row_limit": 1000,                  // Limite righe
        "time_range": "No filter",          // Range temporale
        "granularity": null                 // Granularità temporale
      }
    ],
    "result_format": "json",
    "result_type": "full"
  }
}
```

---
---

## 🔧 Parametri Comuni a Tutti i Chart

### **Colori e Stile**
```json
{
  "color_scheme": "bnbColors",        // Schema colori: "bnbColors", "google", "category20", "d3Category10"
  "show_legend": true,                // Mostra legenda: true/false
  "legend_position": "top"            // Posizione: "top", "bottom", "left", "right"
}
```

### **Formattazione Numeri**
```json
{
  "y_axis_format": ",.0f",           // Formato asse Y: ",.0f", "€,.2f", ".1%", ",.2s"
  "number_format": "€,.2f",          // Formato generico: "€,.2f", ",.0f", ".1%"
  "percent_format": ".1%"            // Formato percentuali: ".1%", ".2%", ".0%"
}
```

### **Filtri e Limiti**
```json
{
  "row_limit": 1000,                 // Limite righe: 100, 500, 1000, 5000
  "adhoc_filters": [],               // Filtri ad-hoc: [{"col": "regione", "op": "==", "val": "Lombardia"}]
  "time_range": "Last year",         // Range: "Last year", "Last 30 days", "No filter"
  "order_desc": true                 // Ordinamento: true = discendente, false = crescente
}
```

### **Configurazione Assi**
```json
{
  "x_axis_label": "Categoria",       // Etichetta asse X: "Regione", "Categoria", "Data"
  "y_axis_label": "Vendite",         // Etichetta asse Y: "Vendite €", "Quantità", "Percentuale"
  "x_axis_showminmax": true,         // Mostra min/max asse X: true/false
  "y_axis_showminmax": true,         // Mostra min/max asse Y: true/false
  "y_axis_bounds": [null, null]      // Limiti asse Y: [0, 1000], [null, null] = auto
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

