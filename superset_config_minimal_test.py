# Minimal Superset Configuration for CSRF Testing
# This config isolates the CSRF issue without OSM/map complications

import os

# Basic Flask Configuration
SECRET_KEY = '2b897f3472fe5e1b1fbc6bd3ef50b7a40d72b776730f4b'  # Using your working v4 secret key

# Database Configuration - Simple SQLite
SQLALCHEMY_DATABASE_URI = 'sqlite:////app/superset_home/superset.db'

# ===== AUTHENTICATION CONFIGURATION =====
# Explicitly set DB Authentication (like your working v4 setup)
from flask_appbuilder.security.manager import AUTH_DB
AUTH_TYPE = AUTH_DB

# Alternative: Test OIDC Authentication (your working v4 approach) 
# from flask_appbuilder.security.manager import AUTH_OID
# AUTH_TYPE = AUTH_OID
# CUSTOM_SECURITY_MANAGER = OIDCSecurityManager  # Uncomment if using OIDC

# ===== CSRF CONFIGURATION =====

# 🔧 DEVELOPMENT MODE: CSRF Disabled (currently active)
WTF_CSRF_ENABLED = False

# 🔒 PRODUCTION MODE: Enable CSRF when ready (uncomment block below)
# WTF_CSRF_ENABLED = True
# WTF_CSRF_TIME_LIMIT = None          # No time limit
# WTF_CSRF_SSL_STRICT = False         # Allow HTTP in development
# WTF_CSRF_SECRET_KEY = '3c9a8f4582gf6f2c2gdc7ce4fg60c8b51e83c887841g5c'

# 🎯 HYBRID MODE: CSRF enabled but exempt API endpoints (alternative)
# WTF_CSRF_ENABLED = True
# WTF_CSRF_TIME_LIMIT = None
# WTF_CSRF_SSL_STRICT = False
# WTF_CSRF_SECRET_KEY = '3c9a8f4582gf6f2c2gdc7ce4fg60c8b51e83c887841g5c'
# WTF_CSRF_EXEMPT_LIST = [
#     '/api/v1/chart/',
#     '/api/v1/dashboard/',
#     '/api/v1/security/login',
#     '/api/v1/dataset/',
#     '/api/v1/slice/'
# ]

# ===== CORS CONFIGURATION =====
ENABLE_CORS = True
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': [
        'http://localhost:8080',    # Superset
        'http://127.0.0.1:8080',    # Superset alternative
        'http://localhost:4200',    # Angular dev server
        'http://localhost:3000'     # React dev server (if needed)
    ]
}

# ===== SESSION CONFIGURATION =====
# Enhanced session security (matching v4 production standards)
SESSION_COOKIE_SECURE = False  # Set to True in HTTPS production
SESSION_COOKIE_HTTPONLY = True  
SESSION_COOKIE_SAMESITE = 'Lax'

# Session timeout configuration
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour (3600 seconds)

# Additional security headers
TALISMAN_ENABLED = False  # Disable for development, enable in production

# ===== MINIMAL FEATURE FLAGS =====
FEATURE_FLAGS = {
    'DASHBOARD_NATIVE_FILTERS': False,  # Minimal features
    'DASHBOARD_CROSS_FILTERS': False,
}

# ===== LOGGING (Minimal) =====
# Use default Superset logging

print("=" * 60)
print("� SUPERSET DEVELOPMENT CONFIGURATION")
print("=" * 60)
print(f"Authentication Type: {AUTH_TYPE}")
print(f"CSRF Protection: {'DISABLED' if not WTF_CSRF_ENABLED else 'ENABLED'}")
print(f"Secret Key: {'✅ SET' if SECRET_KEY and SECRET_KEY != 'YOUR_SECRET_KEY_HERE' else '❌ DEFAULT'}")
print(f"CORS Enabled: {'✅ YES' if ENABLE_CORS else '❌ NO'}")
print(f"Database: SQLite")
print("=" * 60)
print("🎯 CURRENT STATUS:")
print("✅ CSRF: Disabled for development/testing")
print("✅ Bearer tokens: Required for API authentication")
print("✅ Angular ready: No CSRF token needed")
print("✅ PowerShell scripts: Working")
print("=" * 60)
print("� TO ENABLE CSRF LATER:")
print("1. Comment out: WTF_CSRF_ENABLED = False")
print("2. Uncomment desired CSRF block above")
print("3. Restart Superset container")
print("4. Test with CSRF tokens in requests")
print("=" * 60)
print("⚠️  PRODUCTION REMINDER:")
print("Enable CSRF protection before deploying to production!")
print("=" * 60)