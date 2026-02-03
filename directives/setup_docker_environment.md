# Directive: Setup Docker Environment

## Goal
Create a complete Dockerized development environment for the modular CMS system with Laravel backend, Next.js frontend, MySQL database, and supporting services.

## Prerequisites
- Docker 24.0+ installed on host machine
- Docker Compose 2.20+ installed
- Minimum 4GB RAM available
- Port 3000, 8000, 3306, 8025 available

## Inputs
- `project_name` (string): Name of the CMS project (e.g., "my-cms")
- `mysql_root_password` (string): Root password for MySQL
- `mysql_database` (string): Database name (e.g., "cms_db")
- `laravel_app_key` (string, optional): Laravel APP_KEY (generated if not provided)

## Execution Tool
**Script:** `execution/setup_docker_environment.py`

## Process Flow

### 1. Generate docker-compose.yml
Create multi-container setup with:
- **Laravel service** (PHP 8.2-FPM + Nginx)
- **Next.js service** (Node 20 Alpine)
- **MySQL service** (MySQL 8.0)
- **Redis service** (Redis 7 Alpine)
- **Mailhog service** (for email testing)

### 2. Create Docker Network
- Network name: `cms_network`
- Driver: bridge
- Enable DNS resolution between containers

### 3. Setup Persistent Volumes
- `mysql_data`: Database persistence
- `redis_data`: Cache persistence
- `storage_data`: Laravel storage (uploads, logs)

### 4. Generate .env Files
Create environment files for both services:

**Backend (.env):**
```env
APP_NAME="CMS System"
APP_ENV=local
APP_KEY=base64:generated_key_here
APP_DEBUG=true
APP_URL=http://localhost:8000

DB_CONNECTION=mysql
DB_HOST=mysql
DB_PORT=3306
DB_DATABASE=cms_db
DB_USERNAME=root
DB_PASSWORD=secret

CACHE_DRIVER=redis
REDIS_HOST=redis
REDIS_PASSWORD=null
REDIS_PORT=6379

MAIL_MAILER=smtp
MAIL_HOST=mailhog
MAIL_PORT=1025
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

### 5. Create Dockerfiles

**Backend Dockerfile:** (`backend/Dockerfile`)
- Base: `php:8.2-fpm-alpine`
- Install: Composer, PHP extensions (pdo_mysql, redis, gd, etc.)
- Copy application files
- Set permissions
- Run as non-root user

**Frontend Dockerfile:** (`frontend/Dockerfile`)
- Base: `node:20-alpine`
- Install dependencies
- Development mode with hot reload
- Production build support

### 6. Initialize Containers
Run in order:
1. Start MySQL and wait for healthy status
2. Start Redis
3. Start Laravel (run migrations)
4. Start Next.js
5. Start Mailhog

### 7. Verify Setup
Check that all services are running:
- Laravel API: http://localhost:8000/api/health
- Next.js: http://localhost:3000
- Mailhog UI: http://localhost:8025
- MySQL: Connection from Laravel successful

## Expected Outputs

### Success
- All containers running and healthy
- Environment files created and populated
- Networks and volumes configured
- Services accessible on expected ports
- Migration status: All migrations run successfully

**Files created:**
```
cms-system/
├── docker-compose.yml
├── docker-compose.dev.yml
├── .env.example
├── .dockerignore
├── backend/
│   ├── Dockerfile
│   ├── .env
│   └── docker/
│       └── nginx.conf
├── frontend/
│   ├── Dockerfile
│   ├── .env.local
│   └── .dockerignore
└── docs/
    └── docker-setup.md
```

### Failure Scenarios

**1. Port Already in Use**
- Error: "Bind for 0.0.0.0:3000 failed: port is already allocated"
- Solution: Identify process using port, kill it, or change port in docker-compose.yml
- Update directive: Add port conflict detection in script

**2. MySQL Won't Start**
- Error: "MySQL server has gone away"
- Possible causes: Insufficient memory, corrupt volume
- Solution: Check Docker memory settings (min 2GB), remove volume and recreate
- Update directive: Add memory requirement check

**3. Laravel Container Can't Connect to MySQL**
- Error: "SQLSTATE[HY000] [2002] Connection refused"
- Cause: MySQL not fully initialized when Laravel tries to connect
- Solution: Add health check and depends_on with condition
- Update directive: Document container startup order

**4. Next.js Build Fails**
- Error: "Module not found" or "Out of memory"
- Causes: Missing dependencies, insufficient Node memory
- Solution: Increase Node memory (NODE_OPTIONS=--max-old-space-size=4096)
- Update directive: Add Node memory settings to Dockerfile

**5. Permission Issues**
- Error: "Permission denied" for storage or cache directories
- Cause: Docker user doesn't match host user
- Solution: Set correct ownership in Dockerfile or use volume permissions
- Update directive: Document user/group ID mapping for host compatibility

## Edge Cases

### Multi-Platform Builds (M1/M2 Macs)
- Use `platform: linux/amd64` for MySQL and Redis
- Some PHP extensions may need architecture-specific builds
- Add platform detection in script

### Windows WSL2
- Path mapping issues with volumes
- Use WSL2 paths, not Windows paths
- Add WSL2-specific instructions

### Low-Memory Environments
- Reduce container memory limits
- Disable dev tools if needed
- Add memory threshold checks

## Testing Checklist

After running the script, verify:
- [ ] `docker-compose ps` shows all services healthy
- [ ] Laravel API responds at http://localhost:8000/api/health
- [ ] Next.js responds at http://localhost:3000
- [ ] Can create database connection from Laravel
- [ ] Redis connection works (check cache write/read)
- [ ] Mailhog UI accessible at http://localhost:8025
- [ ] Hot reload works for both Laravel and Next.js
- [ ] Logs are accessible via `docker-compose logs [service]`

## Performance Expectations
- Initial setup: 5-10 minutes (includes Docker image builds)
- Subsequent starts: 30-60 seconds
- Hot reload: <2 seconds for code changes

## Maintenance Notes

### Rebuilding Containers
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Clearing Volumes (Fresh Start)
```bash
docker-compose down -v
# This deletes database! Backup first.
```

### Viewing Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f laravel
docker-compose logs -f nextjs
```

### Accessing Container Shell
```bash
docker-compose exec laravel sh
docker-compose exec nextjs sh
```

## Updates to This Directive

### [2025-02-03] Initial creation
- Created comprehensive Docker setup directive
- Defined all services and their configurations

### Future improvements to track:
- If we discover optimal memory settings
- If certain PHP extensions cause issues
- If MySQL initialization takes too long
- If hot reload doesn't work in certain scenarios
- If networking between containers fails

---

**Remember:** Docker environment is the foundation. Everything else builds on this. If containers aren't healthy, stop and fix before proceeding with Laravel or Next.js setup.
