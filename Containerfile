# UBI9 Python S2I image (rootless)
# Official Red Hat Universal Base Image: https://catalog.redhat.com/software/containers/ubi9/python-311
FROM registry.access.redhat.com/ubi9/python-311:latest

# Set working directory (S2I standard)
WORKDIR /opt/app-root/src

# Copy dependency and project files
COPY pyproject.toml uv.lock README.md ./

# Copy application code
COPY src/ ./src/

# Install uv and dependencies using pip (S2I virtualenv)
RUN pip install --no-cache-dir uv && \
    uv pip install "."

# Expose application port
EXPOSE 8000

# Run the application
# TODO: Update to your application entrypoint
CMD ["python", "-m", "my_package"]
