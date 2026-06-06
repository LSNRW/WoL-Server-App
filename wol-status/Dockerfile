FROM python:3.12-slim

WORKDIR /app

# Psutil & FastAPI & Uvicorn für die API; docker-SDK für /containers-Endpoint.
# gcc nur temporär: auf 64-bit (arm64/x86_64) nutzt psutil fertige Wheels,
# auf 32-bit-Pis (armv7) muss es kompiliert werden. Danach wieder entfernen,
# damit das Image schlank bleibt.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && pip install --no-cache-dir fastapi uvicorn psutil docker \
    && apt-get purge -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY app.py /app/app.py

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
