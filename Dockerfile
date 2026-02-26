FROM quay.io/jupyter/minimal-notebook:python-3.11

USER root

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    MCP_TRANSPORT="stdio" \
    HUD_LOG_STREAM="stderr"

WORKDIR /app

# Step 1: Copy dependency files for caching
COPY pyproject.toml /app/

# Step 2: Install all dependencies
RUN pip install --no-cache-dir -e /app/

# Step 3: Copy code
COPY . /app/

# Create directories with proper ownership
RUN mkdir -p /app/data /app/logs /app/shared_data /app/workspace && \
    wget -q https://huggingface.co/datasets/KAKA22/SpreadsheetBench/resolve/main/spreadsheetbench_912_v0.1.tar.gz -O /tmp/data.tar.gz && \
    tar -xzf /tmp/data.tar.gz -C /app/data && \
    rm /tmp/data.tar.gz && \
    chown -R $NB_UID:$NB_GID /app

USER $NB_UID


EXPOSE 8000 8888

ENTRYPOINT ["tini", "-g", "--"]
CMD ["sh", "-c", "\
    jupyter kernelgateway --KernelGatewayApp.ip=0.0.0.0 --KernelGatewayApp.port=8888 >&2 & \
    sleep 5 && cd /app && exec python3 -m env"]
