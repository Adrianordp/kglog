FROM python:3.13-slim

WORKDIR /app

COPY . .

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN uv sync

EXPOSE 9000

CMD ["uv", "run", "python", "main.py"]
