FROM node:22-alpine

WORKDIR /app

# Copy project files into the container.
COPY . .

# Install dependencies only when package.json exists (before Vite scaffold this is a no-op).
RUN if [ -f package.json ]; then npm install; fi

EXPOSE 5173

# Run Vite dev server with host binding for Docker access.
CMD ["sh", "-c", "if [ -f package.json ]; then npm run dev -- --host 0.0.0.0 --port 5173; else echo 'No package.json found in /app. Scaffold frontend first.' && sleep infinity; fi"]
