#!/usr/bin/env python3
"""
Setup Docker Environment for CMS System
Execution script for directives/setup_docker_environment.md
"""

import os
import sys
import subprocess
import secrets
import base64
from pathlib import Path
from typing import Dict, Optional


class DockerEnvironmentSetup:
    def __init__(
        self, project_name: str, mysql_password: str, mysql_database: str
    ):
        self.project_name = project_name
        self.mysql_password = mysql_password
        self.mysql_database = mysql_database
        self.project_root = Path.cwd()

    def generate_app_key(self) -> str:
        """Generate Laravel APP_KEY"""
        random_bytes = secrets.token_bytes(32)
        return f"base64:{base64.b64encode(random_bytes).decode()}"

    def create_docker_compose(self) -> bool:
        """Create docker-compose.yml file"""
        docker_compose_content = f"""version: '3.8'

services:
  # MySQL Database
  mysql:
    image: mysql:8.0
    platform: linux/amd64
    container_name: {self.project_name}_mysql
    ports:
      - "3307:3306"
    environment:
      MYSQL_ROOT_PASSWORD: {self.mysql_password}
      MYSQL_DATABASE: {self.mysql_database}
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - cms_network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p{self.mysql_password}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    platform: linux/amd64
    container_name: {self.project_name}_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - cms_network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Laravel Backend
  laravel:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: {self.project_name}_laravel
    # ports:
    #   - "8000:80"  <-- Removed to enforce access via Next.js proxy
    volumes:
      - ./backend:/var/www/html
      - storage_data:/var/www/html/storage
    environment:
      - APP_ENV=local
      - APP_DEBUG=true
    networks:
      - cms_network
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  # Next.js Frontend
  nextjs:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: {self.project_name}_nextjs
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
    environment:
      - NODE_ENV=development
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
    networks:
      - cms_network
    depends_on:
      - laravel
    restart: unless-stopped

  # Mailhog (Email Testing)
  mailhog:
    image: mailhog/mailhog:latest
    platform: linux/amd64
    container_name: {self.project_name}_mailhog
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI
    networks:
      - cms_network
    restart: unless-stopped

networks:
  cms_network:
    driver: bridge

volumes:
  mysql_data:
    driver: local
  redis_data:
    driver: local
  storage_data:
    driver: local
"""

        try:
            docker_compose_path = self.project_root / "docker-compose.yml"
            with open(docker_compose_path, "w") as f:
                f.write(docker_compose_content)
            print(f"✓ Created docker-compose.yml")
            return True
        except Exception as e:
            print(f"✗ Failed to create docker-compose.yml: {e}")
            return False

    def create_backend_dockerfile(self) -> bool:
        """Create Dockerfile for Laravel backend"""
        dockerfile_content = """FROM php:8.2-fpm-alpine

# Install system dependencies
RUN apk add --no-cache \
    git \
    curl \
    libpng-dev \
    libzip-dev \
    zip \
    unzip \
    nginx \
    supervisor \
    icu-dev

# Install PHP extensions
RUN docker-php-ext-install pdo pdo_mysql zip gd exif intl

# Install Redis extension
RUN apk add --no-cache $PHPIZE_DEPS \
    && pecl install redis \
    && docker-php-ext-enable redis

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set working directory
WORKDIR /var/www/html

# Copy application files
COPY . .

# Set permissions
RUN mkdir -p /var/www/html/storage/framework/views \\
    /var/www/html/storage/framework/cache \\
    /var/www/html/storage/framework/sessions \\
    /var/www/html/storage/logs \\
    /var/www/html/bootstrap/cache
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache

# Install dependencies (if composer.json exists)
RUN if [ -f composer.json ]; then composer install --no-interaction --optimize-autoloader --no-dev; fi

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Copy supervisor configuration
RUN echo "[supervisord]" > /etc/supervisord.conf && \
    echo "nodaemon=true" >> /etc/supervisord.conf && \
    echo "" >> /etc/supervisord.conf && \
    echo "[program:php-fpm]" >> /etc/supervisord.conf && \
    echo "command=php-fpm" >> /etc/supervisord.conf && \
    echo "autostart=true" >> /etc/supervisord.conf && \
    echo "autorestart=true" >> /etc/supervisord.conf && \
    echo "" >> /etc/supervisord.conf && \
    echo "[program:nginx]" >> /etc/supervisord.conf && \
    echo "command=nginx -g 'daemon off;'" >> /etc/supervisord.conf && \
    echo "autostart=true" >> /etc/supervisord.conf && \
    echo "autorestart=true" >> /etc/supervisord.conf

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
"""

        try:
            backend_dir = self.project_root / "backend"
            backend_dir.mkdir(exist_ok=True)

            dockerfile_path = backend_dir / "Dockerfile"
            with open(dockerfile_path, "w") as f:
                f.write(dockerfile_content)
            print(f"✓ Created backend/Dockerfile")
            return True
        except Exception as e:
            print(f"✗ Failed to create backend Dockerfile: {e}")
            return False

    def create_nginx_config(self) -> bool:
        """Create Nginx configuration for Laravel"""
        nginx_config = """user www-data;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    keepalive_timeout 65;
    gzip on;

    server {
        listen 80;
        server_name localhost;
        root /var/www/html/public;

        index index.php index.html;

        location / {
            try_files $uri $uri/ /index.php?$query_string;
        }

        location ~ \\.php$ {
            fastcgi_pass 127.0.0.1:9000;
            fastcgi_index index.php;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include fastcgi_params;
        }

        location ~ /\\.ht {
            deny all;
        }
    }
}
"""

        try:
            docker_dir = self.project_root / "backend" / "docker"
            docker_dir.mkdir(parents=True, exist_ok=True)

            nginx_path = docker_dir / "nginx.conf"
            with open(nginx_path, "w") as f:
                f.write(nginx_config)
            print(f"✓ Created backend/docker/nginx.conf")
            return True
        except Exception as e:
            print(f"✗ Failed to create nginx config: {e}")
            return False

    def create_frontend_dockerfile(self) -> bool:
        """Create Dockerfile for Next.js frontend"""
        dockerfile_content = """FROM node:20-alpine

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
"""

        try:
            frontend_dir = self.project_root / "frontend"
            frontend_dir.mkdir(exist_ok=True)

            dockerfile_path = frontend_dir / "Dockerfile"
            with open(dockerfile_path, "w") as f:
                f.write(dockerfile_content)
            print(f"✓ Created frontend/Dockerfile")
            return True
        except Exception as e:
            print(f"✗ Failed to create frontend Dockerfile: {e}")
            return False

    def create_env_files(self) -> bool:
        """Create environment files for Laravel and Next.js"""
        app_key = self.generate_app_key()

        # Backend .env
        backend_env = f"""APP_NAME="CMS System"
APP_ENV=local
APP_KEY={app_key}
APP_DEBUG=true
APP_URL=http://localhost:8000

LOG_CHANNEL=stack
LOG_LEVEL=debug

DB_CONNECTION=mysql
DB_HOST=mysql
DB_PORT=3306
DB_DATABASE={self.mysql_database}
DB_USERNAME=root
DB_PASSWORD={self.mysql_password}

BROADCAST_DRIVER=log
CACHE_DRIVER=redis
FILESYSTEM_DISK=local
QUEUE_CONNECTION=sync
SESSION_DRIVER=file
SESSION_LIFETIME=120

REDIS_HOST=redis
REDIS_PASSWORD=null
REDIS_PORT=6379

MAIL_MAILER=smtp
MAIL_HOST=mailhog
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
MAIL_FROM_ADDRESS="hello@example.com"
MAIL_FROM_NAME="${{APP_NAME}}"
"""

        # Frontend .env.local
        frontend_env = """NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_SITE_URL=http://localhost:3000
"""

        try:
            # Backend .env
            backend_env_path = self.project_root / "backend" / ".env"
            with open(backend_env_path, "w") as f:
                f.write(backend_env)
            print(f"✓ Created backend/.env")

            # Frontend .env.local
            frontend_env_path = self.project_root / "frontend" / ".env.local"
            with open(frontend_env_path, "w") as f:
                f.write(frontend_env)
            print(f"✓ Created frontend/.env.local")

            # .env.example for both
            backend_example = self.project_root / "backend" / ".env.example"
            with open(backend_example, "w") as f:
                f.write(
                    backend_env.replace(
                        self.mysql_password, "your_password_here"
                    )
                )

            frontend_example = self.project_root / "frontend" / ".env.example"
            with open(frontend_example, "w") as f:
                f.write(frontend_env)

            return True
        except Exception as e:
            print(f"✗ Failed to create .env files: {e}")
            return False

    def create_dockerignore(self) -> bool:
        """Create .dockerignore files"""
        backend_ignore = """node_modules
vendor
.env
.git
.gitignore
storage/logs/*
storage/framework/cache/*
storage/framework/sessions/*
storage/framework/views/*
"""

        frontend_ignore = """node_modules
.next
.git
.gitignore
.env*.local
"""

        try:
            # Backend .dockerignore
            backend_ignore_path = (
                self.project_root / "backend" / ".dockerignore"
            )
            with open(backend_ignore_path, "w") as f:
                f.write(backend_ignore)

            # Frontend .dockerignore
            frontend_ignore_path = (
                self.project_root / "frontend" / ".dockerignore"
            )
            with open(frontend_ignore_path, "w") as f:
                f.write(frontend_ignore)

            print(f"✓ Created .dockerignore files")
            return True
        except Exception as e:
            print(f"✗ Failed to create .dockerignore files: {e}")
            return False

    def start_containers(self) -> bool:
        """Start Docker containers"""
        try:
            print("\n🚀 Starting Docker containers...")
            result = subprocess.run(
                ["docker", "compose", "up", "-d"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print("✓ Containers started successfully")
                return True
            else:
                print(f"✗ Failed to start containers: {result.stderr}")
                return False
        except Exception as e:
            print(f"✗ Error starting containers: {e}")
            return False

    def verify_setup(self) -> bool:
        """Verify all services are running"""
        print("\n🔍 Verifying setup...")

        try:
            result = subprocess.run(
                ["docker", "compose", "ps"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            if "Up" in result.stdout:
                print("✓ All services are running")
                print("\n" + "=" * 50)
                print("🎉 Docker environment setup complete!")
                print("=" * 50)
                print(f"\n📍 Services:")
                print(f"   Laravel API:  http://localhost:8000")
                print(f"   Next.js:      http://localhost:3000")
                print(f"   Mailhog UI:   http://localhost:8025")
                print(f"   MySQL:        localhost:3306")
                print(f"\n📝 Next steps:")
                print(f"   1. Run: cd backend && composer install")
                print(f"   2. Run: cd frontend && npm install")
                print(
                    f"   3. Run migrations: docker compose exec laravel php artisan migrate"
                )
                return True
            else:
                print("⚠ Some services may not be running properly")
                print(result.stdout)
                return False
        except Exception as e:
            print(f"✗ Error verifying setup: {e}")
            return False

    def run(self) -> bool:
        """Execute full setup process"""
        print("🔧 Setting up Docker environment...")
        print(f"Project: {self.project_name}")
        print(f"Database: {self.mysql_database}\n")

        steps = [
            ("Creating docker-compose.yml", self.create_docker_compose),
            ("Creating backend Dockerfile", self.create_backend_dockerfile),
            ("Creating nginx config", self.create_nginx_config),
            ("Creating frontend Dockerfile", self.create_frontend_dockerfile),
            ("Creating environment files", self.create_env_files),
            ("Creating .dockerignore files", self.create_dockerignore),
            ("Starting containers", self.start_containers),
            ("Verifying setup", self.verify_setup),
        ]

        for step_name, step_func in steps:
            if not step_func():
                print(f"\n❌ Setup failed at: {step_name}")
                return False

        return True


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Setup Docker environment for CMS"
    )
    parser.add_argument(
        "--project-name", default="cms-system", help="Project name"
    )
    parser.add_argument(
        "--mysql-password", default="secret", help="MySQL root password"
    )
    parser.add_argument(
        "--mysql-database", default="cms_db", help="MySQL database name"
    )

    args = parser.parse_args()

    setup = DockerEnvironmentSetup(
        project_name=args.project_name,
        mysql_password=args.mysql_password,
        mysql_database=args.mysql_database,
    )

    success = setup.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
