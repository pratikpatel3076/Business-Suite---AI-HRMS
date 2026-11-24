FROM python:3.12-slim

LABEL org.opencontainers.image.title="Gemeinsam API"
LABEL org.opencontainers.image.description="Gemeinsam backend API"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]

EXPOSE 8000

# Auth rate limits use the client IP, so Uvicorn must trust the reverse proxy
# that supplies X-Forwarded-For. Set FORWARDED_ALLOW_IPS to the proxy/load
# balancer CIDR(s) in production; never use "*" on a publicly exposed API.
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips \"${FORWARDED_ALLOW_IPS:-127.0.0.1}\""]
