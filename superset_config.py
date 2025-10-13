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

# Enable CORS for API access and map tile sources
ENABLE_CORS = True
CORS_OPTIONS: Dict[str, Any] = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': [
        # Local development origins
        'http://localhost:8080',   # Direct Superset access (your current setup)
        'http://localhost:8088',   # Standard Superset port
        'http://localhost:4200',   # Angular dev server
        'http://127.0.0.1:8080',   # Alternative localhost format
        'http://127.0.0.1:8088',   # Alternative localhost format
        
        # External tile sources for maps
        "https://tile.openstreetmap.org",
        "https://a.tile.openstreetmap.org", 
        "https://b.tile.openstreetmap.org",
        "https://c.tile.openstreetmap.org",
        "https://tile.osm.ch",
        
        # Production origins (if needed)
        'https://dss-coll.regione.puglia.it',
        'https://superset.regione.puglia.it',
        
        # Add your custom tile URLs here if needed
        # "https://your_personal_url/{z}/{x}/{y}.png",
    ]
}

# Content Security Policy for map tiles and API access
TALISMAN_CONFIG = {
    "content_security_policy": {
        "default-src": ["'self'", "http://localhost:*", "http://127.0.0.1:*"],
        "script-src": [
            "'self'",
            "'unsafe-inline'",
            "'unsafe-eval'",
            "https://api.mapbox.com",
            "http://localhost:*",
            "http://127.0.0.1:*",
        ],
        "style-src": [
            "'self'",
            "'unsafe-inline'",
            "http://localhost:*",
            "http://127.0.0.1:*",
        ],
        "img-src": [
            "'self'",
            "data:",
            "https://tile.openstreetmap.org",
            "https://a.tile.openstreetmap.org",
            "https://b.tile.openstreetmap.org", 
            "https://c.tile.openstreetmap.org",
            "https://tile.osm.ch",
            "http://localhost:*",
            "http://127.0.0.1:*",
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
            "http://localhost:*",
            "http://127.0.0.1:*",
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

# CSRF Configuration for API access
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None  # No time limit for CSRF tokens
WTF_CSRF_SSL_STRICT = False  # Allow HTTP for localhost development

# Session Configuration
SESSION_COOKIE_SECURE = False  # Allow cookies over HTTP for localhost
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'  # Less strict for development

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

print("=" * 60)
print("🔧 CRITICAL: CORS & API CONFIGURATION STATUS")
print("=" * 60)
print(f"CORS Enabled: {ENABLE_CORS}")
print(f"CORS Supports Credentials: {CORS_OPTIONS.get('supports_credentials', False)} {'✅' if CORS_OPTIONS.get('supports_credentials') else '❌'}")
print(f"CORS Allow Headers: {CORS_OPTIONS.get('allow_headers', 'Not set')} {'✅' if CORS_OPTIONS.get('allow_headers') == ['*'] else '❌'}")

# Check for localhost:8080 specifically
has_localhost_8080 = any('localhost:8080' in origin for origin in CORS_OPTIONS.get('origins', []))
print(f"localhost:8080 in CORS origins: {has_localhost_8080} {'✅' if has_localhost_8080 else '❌'}")

print(f"CSRF Enabled: {WTF_CSRF_ENABLED} {'✅' if WTF_CSRF_ENABLED else '❌'}")
print(f"CSRF SSL Strict: {WTF_CSRF_SSL_STRICT} {'✅ (HTTP OK)' if not WTF_CSRF_SSL_STRICT else '❌ (HTTPS Only)'}")
print(f"Session Cookie Secure: {SESSION_COOKIE_SECURE} {'✅ (HTTP OK)' if not SESSION_COOKIE_SECURE else '❌ (HTTPS Only)'}")

if (ENABLE_CORS and CORS_OPTIONS.get('supports_credentials') and has_localhost_8080 and WTF_CSRF_ENABLED and not WTF_CSRF_SSL_STRICT):
    print("\n🎉 ALL API SETTINGS CONFIGURED CORRECTLY FOR localhost:8080!")
else:
    print("\n⚠️ Some API settings may cause issues - check above")

print("=" * 60)

print("\n=== SUPERSET OSM CONFIGURATION LOADED ===")
print(f"DECKGL_BASE_MAP configured with {len(DECKGL_BASE_MAP)} tile sources:")
for idx, (url, name) in enumerate(DECKGL_BASE_MAP, 1):
    print(f"  {idx}. {name}: {url}")
print("\n🔄 READY FOR API TESTING - Configuration loaded successfully!")
print("=" * 60)