# Superset Configuration for OSM Map Tiles Testing (CORS Disabled)
# Based on official documentation: https://superset.apache.org/docs/configuration/map-tiles

import os
from typing import Any, Dict, List

# Flask App Secret Key
SECRET_KEY = '2b897f3472fe5e1b1fbc6bd3ef50b7a40d72b776730f4b'

# Database Configuration - Using SQLite for simplicity
SQLALCHEMY_DATABASE_URI = 'sqlite:////app/superset_home/superset.db'

# Redis Configuration
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

# Cache Configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': REDIS_HOST,
    'CACHE_REDIS_PORT': REDIS_PORT,
    'CACHE_REDIS_DB': 1,
    'CACHE_REDIS_URL': f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
}

# ===== OSM MAP TILES CONFIGURATION =====
# Based on official Superset documentation: https://superset.apache.org/docs/configuration/map-tiles

# Default configuration from Superset docs (includes OSM by default)
DECKGL_BASE_MAP = [
    ['https://tile.openstreetmap.org/{z}/{x}/{y}.png', 'Streets (OSM)'],
    ['https://tile.osm.ch/osm-swiss-style/{z}/{x}/{y}.png', 'Topography (OSM)'],
    ['mapbox://styles/mapbox/streets-v9', 'Streets'],
    ['mapbox://styles/mapbox/dark-v9', 'Dark'],
    ['mapbox://styles/mapbox/light-v9', 'Light'],
    ['mapbox://styles/mapbox/satellite-streets-v9', 'Satellite Streets'],
    ['mapbox://styles/mapbox/satellite-v9', 'Satellite'],
    ['mapbox://styles/mapbox/outdoors-v9', 'Outdoors'],
]

# Disable CORS for now to avoid flask-cors dependency issues
# ENABLE_CORS = False

# Try to enable CORS if flask-cors is available (as per official docs)
try:
    from flask_cors import CORS
    ENABLE_CORS = True
    CORS_OPTIONS: dict[Any, Any] = {
        "origins": [
            "https://tile.openstreetmap.org",
            "https://tile.osm.ch",
        ]
    }
    cors_status = "True (flask-cors available)"
except ImportError:
    ENABLE_CORS = False
    cors_status = "False (flask-cors not available)"

# Content Security Policy for map tiles (simplified)
TALISMAN_CONFIG = {
    "force_https": False,  # Disable HTTPS redirect
    "content_security_policy": {
        "default-src": ["'self'"],
        "script-src": [
            "'self'",
            "'unsafe-inline'",
            "'unsafe-eval'",
        ],
        "style-src": [
            "'self'",
            "'unsafe-inline'",
        ],
        "img-src": [
            "'self'",
            "data:",
            "https://tile.openstreetmap.org",
            "https://tile.osm.ch",
            "https://api.mapbox.com",
        ],
        "connect-src": [
            "'self'",
            "https://api.mapbox.com",
            "https://events.mapbox.com",
            "https://tile.openstreetmap.org",
            "https://tile.osm.ch",
        ],
    }
}

# Additional Superset Configuration
FEATURE_FLAGS = {
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'ENABLE_TEMPLATE_PROCESSING': True,
    'GENERIC_CHART_AXES': True,
}

# Row Level Security
ROW_LEVEL_SECURITY_VERBOSE = True

# WebDriver for reports
WEBDRIVER_BASEURL = "http://superset:8088/"

# Email Configuration (optional, for testing alerts)
EMAIL_NOTIFICATIONS = False

print("=== SUPERSET OSM CONFIGURATION LOADED ===")
print(f"DECKGL_BASE_MAP configured with {len(DECKGL_BASE_MAP)} tile sources:")
for idx, (url, name) in enumerate(DECKGL_BASE_MAP, 1):
    print(f"  {idx}. {name}: {url}")
print("==========================================")

# Additional debug info
print(f"CORS Enabled: {cors_status}")
print(f"Database URI: {SQLALCHEMY_DATABASE_URI}")
print("Configuration loaded successfully!")