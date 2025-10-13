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

# ===== CSRF CONFIGURATION TESTING =====

# Test 1: Completely disable CSRF (quick test)
WTF_CSRF_ENABLED = False  # START WITH THIS

# Test 2: If Test 1 works, try enabling CSRF with exemptions
# WTF_CSRF_ENABLED = True
# WTF_CSRF_EXEMPT_LIST = [
#     '/api/v1/chart/',
#     '/api/v1/dashboard/', 
#     '/api/v1/slice/',
#     '/api/v1/*'
# ]

# Test 3: CSRF with relaxed settings
# WTF_CSRF_TIME_LIMIT = None
# WTF_CSRF_SSL_STRICT = False
# WTF_CSRF_CHECK_DEFAULT = False

# ===== MINIMAL CORS CONFIGURATION =====
ENABLE_CORS = True
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': ['http://localhost:8080', 'http://127.0.0.1:8080']
}

# ===== SESSION CONFIGURATION =====
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True  
SESSION_COOKIE_SAMESITE = 'Lax'

# ===== MINIMAL FEATURE FLAGS =====
FEATURE_FLAGS = {
    'DASHBOARD_NATIVE_FILTERS': False,  # Minimal features
    'DASHBOARD_CROSS_FILTERS': False,
}

# ===== LOGGING (Minimal) =====
# Use default Superset logging

print("=" * 60)
print("🧪 MINIMAL CSRF TEST CONFIGURATION")
print("=" * 60)
print(f"Authentication Type: {AUTH_TYPE}")
print(f"CSRF Enabled: {WTF_CSRF_ENABLED}")
print(f"Secret Key: {'SET' if SECRET_KEY and SECRET_KEY != 'YOUR_SECRET_KEY_HERE' else 'DEFAULT'}")
print(f"CORS Enabled: {ENABLE_CORS}")
print("=" * 60)
print("🎯 TEST PLAN:")
print("1. Start with CSRF disabled (WTF_CSRF_ENABLED = False)")
print("2. If API works, gradually enable CSRF features")
print("3. Compare DB auth vs OIDC auth behavior")
print("=" * 60)