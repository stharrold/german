# Containerfile for german
# Python 3.11 + uv environment for development and CI/CD
#
# Build:  podman build -t german .
# Run:    podman run --rm -v .:/app german <command>
# Shell:  podman run --rm -it -v .:/app german bash

FROM python:3.11-slim

LABEL maintainer="stharrold"
LABEL description="German language learning development environment with uv + Python 3.11"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy dependency files first (for layer caching)
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen 2>/dev/null || uv sync

# Copy project files
COPY . .

# Set default command
CMD ["bash"]
