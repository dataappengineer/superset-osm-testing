FROM apache/superset:5.0.0

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies including flask-cors in the virtual environment
RUN /app/.venv/bin/pip install --no-cache-dir \
    flask-cors==5.0.1 \
    pyarrow \
    psycopg2-binary

# Create pythonpath directory 
RUN mkdir -p /app/pythonpath

# Copy configuration file
COPY superset_config.py /app/pythonpath/superset_config.py

# Copy and setup entrypoint script
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Set permissions 
RUN chown -R superset:superset /app/pythonpath

# Set environment variables
ENV SUPERSET_CONFIG_PATH=/app/pythonpath/superset_config.py
ENV PYTHONPATH=/app/pythonpath:$PYTHONPATH

# Switch back to superset user
USER superset

# Expose port
EXPOSE 8088