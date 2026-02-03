FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN if [ -f package.json ]; then npm install; fi

# Copy application files
COPY . .

EXPOSE 3000

# Development mode with hot reload
CMD sh -c "if [ -f package.json ]; then npm run dev; else echo 'No package.json found. Waiting for setup...' && tail -f /dev/null; fi"
