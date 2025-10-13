# Superset Configuration for OSM Map Tiles Testing
# Based on official documentation: https://superset.apache.org/docs/configuration/map-tiles

import os
from typing import Any, Dict, List

# Flask App Secret Key
SECRET_KEY = os.environ.get('SUPERSET_SECRET_KEY', 'YOUR_SECRET_KEY_HERE')

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
# This is the key configuration to test OSM support in Superset 5.0.0

# Configure map tiles with OpenStreetMap support
DECKGL_BASE_MAP = [
    # Primary OpenStreetMap tile server
    ['https://tile.openstreetmap.org/{z}/{x}/{y}.png', 'Streets (OSM)'],
    
    # Alternative OSM servers for redundancy
    ['https://a.tile.openstreetmap.org/{z}/{x}/{y}.png', 'Streets OSM (Server A)'],
    ['https://b.tile.openstreetmap.org/{z}/{x}/{y}.png', 'Streets OSM (Server B)'],
    ['https://c.tile.openstreetmap.org/{z}/{x}/{y}.png', 'Streets OSM (Server C)'],
    
    # OSM Swiss Style (topographic)
    ['https://tile.osm.ch/osm-swiss-style/{z}/{x}/{y}.png', 'Topography (OSM)'],
    
    # Custom tile server example (commented out)
    # ['tile://https://your_personal_url/{z}/{x}/{y}.png', 'Custom Tiles'],
]

# Enable CORS for map tile sources
ENABLE_CORS = True
CORS_OPTIONS: Dict[str, Any] = {
    "origins": [
        "https://tile.openstreetmap.org",
        "https://a.tile.openstreetmap.org", 
        "https://b.tile.openstreetmap.org",
        "https://c.tile.openstreetmap.org",
        "https://tile.osm.ch",
        # Add your custom tile URLs here if needed
        # "https://your_personal_url/{z}/{x}/{y}.png",
    ]
}

# Content Security Policy for map tiles
TALISMAN_CONFIG = {
    "content_security_policy": {
        "default-src": ["'self'"],
        "script-src": [
            "'self'",
            "'unsafe-inline'",
            "'unsafe-eval'",
            "https://api.mapbox.com",
        ],
        "style-src": [
            "'self'",
            "'unsafe-inline'",
        ],
        "img-src": [
            "'self'",
            "data:",
            "https://tile.openstreetmap.org",
            "https://a.tile.openstreetmap.org",
            "https://b.tile.openstreetmap.org", 
            "https://c.tile.openstreetmap.org",
            "https://tile.osm.ch",
        ],
        "connect-src": [
            "'self'",
            "https://api.mapbox.com",
            "https://events.mapbox.com",
            "https://tile.openstreetmap.org",
            "https://a.tile.openstreetmap.org",
            "https://b.tile.openstreetmap.org",
            "https://c.tile.openstreetmap.org", 
            "https://tile.osm.ch",
            # Add your custom tile URLs here if needed
            # "https://your_personal_url/{z}/{x}/{y}.png",
        ],
    }
}

# Development version of Talisman config (less restrictive for testing)
TALISMAN_CONFIG_DEV = {
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
            "*",  # Allow all image sources in dev
        ],
        "connect-src": [
            "'self'",
            "*",  # Allow all connections in dev
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

# Logging Configuration - Remove complex logging setup that's causing issues
# Use default Superset logging instead
# LOGGING_CONFIGURATOR = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'default': {
#             'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#         }
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'default',
#             'stream': 'ext://sys.stdout'
#         }
#     },
#     'root': {
#         'level': 'INFO',
#         'handlers': ['console']
#     }
# }

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