FROM python:3.10.4-alpine3.15

RUN apk add curl && \
    curl -LO "https://dl.k8s.io/release/v1.24.0/bin/linux/amd64/kubectl"  && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl && \
    addgroup -S appuser && \
    adduser -S appuser -G appuser --uid 3344

COPY --chown=appuser:appuser ./src /home/appuser

USER appuser
WORKDIR /home/appuser

RUN pip install --user --no-cache-dir -r requirements.txt
