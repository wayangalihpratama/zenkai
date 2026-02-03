# Directive: Deploy to Indonesian/Singapore Hosting

## Goal
Deploy the complete CMS system to production hosting in Indonesia or Singapore, with proper security, performance optimization, and monitoring.

## Prerequisites
- Docker images built and tested locally
- Domain name registered
- Hosting provider account (Niagahoster, Dewaweb, DigitalOcean, or AWS)
- SSL certificate (Let's Encrypt)
- Database backups created

## Inputs
- `hosting_provider` (enum): "niagahoster" | "dewaweb" | "digitalocean" | "aws"
- `domain_name` (string): Production domain (e.g., "example.com")
- `environment` (enum): "staging" | "production"

## Execution Tool
**Script:** `execution/deploy_production.py`

## Deployment Options

### Option 1: VPS with Docker (Recommended)

**Providers:**
- DigitalOcean Singapore ($12/month - 2GB RAM)
- AWS Lightsail Singapore ($10/month - 2GB RAM)
- Vultr Singapore ($12/month - 2GB RAM)

**Specs needed:**
- 2GB RAM minimum (4GB recommended)
- 2 CPU cores
- 50GB SSD storage
- Ubuntu 22.04 LTS

### Option 2: Shared Hosting with cPanel

**Providers:**
- Niagahoster Indonesia (Rp 100k/month)
- Dewaweb Indonesia (Rp 120k/month)

**Limitations:**
- May not support Docker
- Need to deploy without containers
- Limited customization

### Option 3: Managed Kubernetes (Enterprise)

**Providers:**
- Google Kubernetes Engine (GKE) Singapore
- AWS EKS Singapore

**Use case:** High traffic, multiple instances

## Deployment Process

### 1. Server Preparation (VPS)

#### SSH into Server
```bash
ssh root@your-server-ip
```

#### Update System
```bash
apt update && apt upgrade -y
```

#### Install Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

#### Install Docker Compose
```bash
apt install docker-compose-plugin -y
```

#### Create Deploy User
```bash
adduser deployer
usermod -aG docker deployer
```

### 2. Repository Setup

#### Clone Repository
```bash
su - deployer
git clone <repository-url> /var/www/cms-system
cd /var/www/cms-system
```

#### Configure Environment
```bash
cp .env.example .env
nano .env

# Update production values:
# - APP_ENV=production
# - APP_DEBUG=false
# - APP_URL=https://yourdomain.com
# - Database credentials
# - Mail settings
# - Payment gateway keys
```

### 3. SSL Certificate (Let's Encrypt)

#### Install Certbot
```bash
apt install certbot python3-certbot-nginx -y
```

#### Generate Certificate
```bash
certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

#### Auto-renewal
```bash
certbot renew --dry-run
```

### 4. Build Production Images

#### Create Production Docker Compose
**docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    platform: linux/amd64
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
    volumes:
      - mysql_prod_data:/var/lib/mysql
    networks:
      - cms_prod_network

  redis:
    image: redis:7-alpine
    platform: linux/amd64
    restart: always
    volumes:
      - redis_prod_data:/data
    networks:
      - cms_prod_network

  laravel:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    restart: always
    volumes:
      - storage_prod_data:/var/www/html/storage
    environment:
      - APP_ENV=production
      - APP_DEBUG=false
    depends_on:
      - mysql
      - redis
    networks:
      - cms_prod_network

  nextjs:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    restart: always
    environment:
      - NODE_ENV=production
    depends_on:
      - laravel
    networks:
      - cms_prod_network

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - storage_prod_data:/var/www/html/storage
    depends_on:
      - laravel
      - nextjs
    networks:
      - cms_prod_network

networks:
  cms_prod_network:
    driver: bridge

volumes:
  mysql_prod_data:
  redis_prod_data:
  storage_prod_data:
```

#### Production Dockerfile for Laravel
**backend/Dockerfile.prod:**
```dockerfile
FROM php:8.2-fpm-alpine

RUN apk add --no-cache \
    git curl libpng-dev libzip-dev zip unzip nginx supervisor

RUN docker-php-ext-install pdo pdo_mysql zip gd

RUN pecl install redis && docker-php-ext-enable redis

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

COPY . .

RUN composer install --no-interaction --optimize-autoloader --no-dev

RUN php artisan config:cache && \
    php artisan route:cache && \
    php artisan view:cache

RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache

EXPOSE 80

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
```

#### Production Dockerfile for Next.js
**frontend/Dockerfile.prod:**
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
```

### 5. Nginx Configuration

**nginx/nginx.conf:**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream laravel_backend {
        server laravel:80;
    }

    upstream nextjs_frontend {
        server nextjs:3000;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$host$request_uri;
    }

    # HTTPS Server
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Next.js Frontend
        location / {
            proxy_pass http://nextjs_frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }

        # Laravel API
        location /api {
            proxy_pass http://laravel_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Laravel Admin
        location /admin {
            proxy_pass http://laravel_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Static files from Laravel storage
        location /storage {
            proxy_pass http://laravel_backend;
        }

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    }
}
```

### 6. Deploy Application

#### Build and Start Containers
```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

#### Run Migrations
```bash
docker-compose -f docker-compose.prod.yml exec laravel php artisan migrate --force
```

#### Clear Caches
```bash
docker-compose -f docker-compose.prod.yml exec laravel php artisan optimize:clear
docker-compose -f docker-compose.prod.yml exec laravel php artisan config:cache
docker-compose -f docker-compose.prod.yml exec laravel php artisan route:cache
```

#### Create Admin User
```bash
docker-compose -f docker-compose.prod.yml exec laravel php artisan make:filament-user
```

### 7. Cloudflare Setup (Recommended)

#### DNS Configuration
```
Type  | Name | Content           | Proxy
------|------|-------------------|-------
A     | @    | your-server-ip    | Yes
A     | www  | your-server-ip    | Yes
```

#### Cloudflare Settings
- SSL/TLS: Full (strict)
- Always Use HTTPS: On
- Automatic HTTPS Rewrites: On
- Minimum TLS Version: 1.2
- Cache Level: Standard
- Browser Cache TTL: 4 hours

### 8. Monitoring & Logging

#### Install Monitoring Tools
```bash
# Install Netdata for server monitoring
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
```

#### Application Logs
```bash
# View Laravel logs
docker-compose -f docker-compose.prod.yml logs -f laravel

# View Next.js logs
docker-compose -f docker-compose.prod.yml logs -f nextjs

# View Nginx logs
docker-compose -f docker-compose.prod.yml logs -f nginx
```

#### Log Rotation
Create `/etc/logrotate.d/cms-system`:
```
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    missingok
    delaycompress
    copytruncate
}
```

### 9. Backup Strategy

#### Database Backup Script
**scripts/backup.sh:**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/cms-system"
mkdir -p $BACKUP_DIR

# Backup database
docker-compose -f docker-compose.prod.yml exec -T mysql \
  mysqldump -u root -p${MYSQL_ROOT_PASSWORD} ${MYSQL_DATABASE} \
  > $BACKUP_DIR/db_backup_$DATE.sql

# Backup storage
tar -czf $BACKUP_DIR/storage_backup_$DATE.tar.gz \
  ./backend/storage

# Remove backups older than 30 days
find $BACKUP_DIR -mtime +30 -delete
```

#### Automated Backups (Cron)
```bash
crontab -e

# Daily backup at 2 AM
0 2 * * * /var/www/cms-system/scripts/backup.sh
```

### 10. Performance Optimization

#### Enable OPcache (Laravel)
Add to `php.ini`:
```ini
opcache.enable=1
opcache.memory_consumption=256
opcache.max_accelerated_files=20000
opcache.validate_timestamps=0
```

#### Redis Caching
```bash
# Laravel config
CACHE_DRIVER=redis
SESSION_DRIVER=redis
```

#### CDN Integration
Upload static assets to Cloudflare CDN:
```bash
# Sync Next.js static files
aws s3 sync frontend/public s3://cdn-bucket/
```

## Security Hardening

### 1. Firewall Setup
```bash
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw enable
```

### 2. Fail2Ban
```bash
apt install fail2ban -y
systemctl enable fail2ban
```

### 3. Environment Variables
Never commit `.env` files. Use secrets management:
```bash
# Store secrets securely
chmod 600 .env
```

### 4. Regular Updates
```bash
# Monthly security updates
apt update && apt upgrade -y
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

## Testing Checklist

After deployment, verify:
- [ ] Website accessible via HTTPS
- [ ] SSL certificate valid
- [ ] All pages load correctly
- [ ] API endpoints working
- [ ] Admin panel accessible
- [ ] Database connections stable
- [ ] Images displaying correctly
- [ ] Forms submitting properly
- [ ] Payment gateway functional (test mode first)
- [ ] Email sending working
- [ ] Logs being written
- [ ] Backups running on schedule

## Performance Expectations

- Page load time: <2 seconds
- API response time: <200ms
- Uptime: 99.9%
- Database query time: <50ms

## Rollback Plan

If deployment fails:
```bash
# Stop current deployment
docker-compose -f docker-compose.prod.yml down

# Restore previous version
git checkout <previous-commit>
docker-compose -f docker-compose.prod.yml up -d

# Restore database backup
docker-compose -f docker-compose.prod.yml exec -T mysql \
  mysql -u root -p${MYSQL_ROOT_PASSWORD} ${MYSQL_DATABASE} \
  < /var/backups/cms-system/db_backup_YYYYMMDD.sql
```

## Indonesian-Specific Considerations

### Payment Gateway (Midtrans)
```env
MIDTRANS_SERVER_KEY=your_production_server_key
MIDTRANS_CLIENT_KEY=your_production_client_key
MIDTRANS_IS_PRODUCTION=true
```

### Local CDN
Consider using BunnyCDN Singapore for better latency in Indonesia.

### Timezone
```env
APP_TIMEZONE=Asia/Jakarta
```

## Updates to This Directive

### [2025-02-03] Initial creation
- Created comprehensive deployment directive
- Defined hosting options for Indonesia/Singapore
- Planned security and monitoring strategies

### Future improvements to track:
- Actual deployment times
- Performance metrics achieved
- Issues encountered during deployment
- Optimization techniques that work best

---

**Remember:** Always test on staging environment first. Keep backups. Monitor closely after deployment.
