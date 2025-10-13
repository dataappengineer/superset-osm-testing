# Superset OSM Testing Environment

This repository contains a complete testing environment for Apache Superset with OpenStreetMap (OSM) tiles configuration and API query examples.

## 🎯 Project Overview

**Primary Goal**: Test if Apache Superset v5.0.0/v6.0.0rc2 supports OpenStreetMap tiles through manual configuration.

**Result**: ✅ **YES! OSM tiles are fully supported** through manual configuration in both versions.

## 🗺️ What's Included

- **Docker Compose setup** for Superset 5.0.0 and 6.0.0rc2
- **OSM tiles configuration** with 5 different tile sources
- **CORS-enabled setup** for API access
- **Example data** and test datasets
- **API documentation** for query execution
- **Working configuration files**

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git installed

### Setup Steps

1. **Clone the repository:**
```bash
git clone https://github.com/dataappengineer/superset-osm-testing.git
cd superset-osm-testing
```

2. **Start Superset:**
```bash
docker-compose up -d
```

3. **Wait for startup** (2-3 minutes for first run)

4. **Access Superset:**
- URL: http://localhost:8080
- Username: `admin`
- Password: `admin`

## 🗺️ OSM Tiles Configuration

The configuration includes 5 OpenStreetMap tile sources:

1. **Streets (OSM)**: https://tile.openstreetmap.org/{z}/{x}/{y}.png
2. **Streets OSM (Server A)**: https://a.tile.openstreetmap.org/{z}/{x}/{y}.png  
3. **Streets OSM (Server B)**: https://b.tile.openstreetmap.org/{z}/{x}/{y}.png
4. **Streets OSM (Server C)**: https://c.tile.openstreetmap.org/{z}/{x}/{y}.png
5. **Topography (OSM)**: https://tile.osm.ch/osm-swiss-style/{z}/{x}/{y}.png

### Testing OSM Tiles

1. Go to **Charts** → **Create New Chart**
2. Select **`long_lat`** dataset
3. Choose **`deck.gl Scatterplot`** visualization
4. Configure:
   - **Longitude**: `LON` column
   - **Latitude**: `LAT` column
5. **Check "Map Style" dropdown** - you should see all OSM options!

## 📊 API Usage

### Authentication
```bash
# Login to get access token
curl -X POST "http://localhost:8080/api/v1/security/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin", "provider": "db"}'
```

### Execute Queries
```bash
# Execute chart query with dataset ID
curl -X POST "http://localhost:8080/api/v1/chart/data" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
  -d '{
    "queries": [{
      "datasource": "1__table",
      "viz_type": "table", 
      "groupby": ["LAT", "LON"],
      "row_limit": 100
    }]
  }'
```

## 📁 File Structure

```
superset-osm-testing/
├── docker-compose.yml              # Docker Compose configuration
├── superset_config_no_cors.py      # Superset configuration with OSM tiles
├── superset_config.py              # Alternative configuration
├── docker-entrypoint.sh            # Custom entrypoint script
├── Dockerfile                      # Custom Docker image
├── data/                          # Test data files
│   ├── european_cities.csv        # Sample geographic data
│   ├── regional_stats.csv         # Sample statistical data
│   └── create_test_tables.sql     # Database initialization
├── scripts/                       # Utility scripts
│   ├── init_superset.sh           # Superset initialization
│   ├── start_unix.sh              # Unix startup script
│   └── start_windows.bat          # Windows startup script
├── superset_home/                 # Superset data directory (auto-created)
└── README.md                      # This file
```

## 🔧 Configuration Files

### `docker-compose.yml`
- Uses `apache/superset:6.0.0rc2` image
- Includes Redis cache
- Mounts OSM configuration
- Auto-installs flask-cors

### `superset_config_no_cors.py`
- **DECKGL_BASE_MAP** with OSM tiles
- **CORS configuration** for API access
- **TALISMAN_CONFIG** with proper CSP headers
- **Cache configuration** with Redis

## 🧪 Version Testing

### Superset 5.0.0
```yaml
image: apache/superset:5.0.0
```

### Superset 6.0.0rc2  
```yaml
image: apache/superset:6.0.0rc2
```

Both versions support OSM tiles with the same configuration!

## 🔍 Troubleshooting

### Common Issues

1. **OSM tiles not showing in UI:**
   - Clear browser cache (Ctrl+F5)
   - Try incognito mode
   - Ensure you're using deck.gl visualization types

2. **HTTPS redirect errors:**
   - Configuration includes `"force_https": false`
   - Use HTTP: `http://localhost:8080` (not HTTPS)

3. **CORS errors:**
   - flask-cors is auto-installed in entrypoint
   - CORS_OPTIONS configured for OSM domains

### Container Logs
```bash
docker-compose logs superset -f
```

Look for: **"=== SUPERSET OSM CONFIGURATION LOADED ==="**

## 📝 API Documentation

### Key Endpoints

| Endpoint | Purpose | Method |
|----------|---------|--------|
| `/api/v1/security/login` | Authentication | POST |
| `/api/v1/dataset/` | List datasets | GET |
| `/api/v1/chart/data` | Execute queries | POST |
| `/api/v1/sqllab/execute` | Execute SQL | POST |

### Query Structure
```json
{
  "queries": [{
    "datasource": "DATASET_ID__table",
    "viz_type": "table",
    "groupby": ["column1", "column2"],
    "metrics": ["count", "sum__amount"],
    "adhoc_filters": [...],
    "row_limit": 1000
  }]
}
```

## 🎉 Success Metrics

✅ **OSM Configuration Loading**: 5 tile sources configured  
✅ **API Access**: Full REST API with CORS enabled  
✅ **Example Data**: Includes geographic test datasets  
✅ **Multi-Version**: Works with both 5.0.0 and 6.0.0rc2  
✅ **Documentation**: Complete setup and usage guide  

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is for testing and educational purposes.

---

**Repository**: https://github.com/dataappengineer/superset-osm-testing  
**Created**: October 2025  
**Testing Result**: ✅ **Superset DOES support OpenStreetMap tiles!** 🗺️