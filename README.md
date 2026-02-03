# CMS System - Modular Headless CMS

A production-ready, Dockerized CMS system with Laravel backend and Next.js frontend, supporting multiple website types: Shop, Travel Agency, Restaurant, and Corporate.

## 🎯 Features

### Core Features
- **Headless Architecture**: Laravel API + Next.js frontend
- **Multi-tenant**: Support for multiple website types
- **Dockerized**: Complete development environment
- **SEO Optimized**: Server-side rendering, JSON-LD schemas, meta tags
- **Admin Panel**: Laravel Filament for easy content management
- **Mobile First**: Responsive design out of the box

### Website Types

#### 🛍️ E-commerce Shop
- Product catalog with categories
- Shopping cart and checkout
- Payment integration (Midtrans)
- Inventory management
- Multi-currency support

#### ✈️ Travel Agency
- Tour packages with itineraries
- Booking system
- Multi-day trip planning
- Multi-language support
- Gallery and testimonials

#### 🍽️ Restaurant
- Digital menu
- Table reservations
- Online ordering
- Food delivery integration
- Multi-location support

#### 🏢 Corporate
- Services showcase
- Portfolio/case studies
- Team profiles
- Blog/news section
- Career listings

## 🚀 Quick Start

### Prerequisites
- Docker 24.0+
- Docker Compose 2.20+
- 4GB RAM minimum
- Ports 3000, 8000, 3306, 8025 available

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd cms-system
```

2. **Setup Docker environment**
```bash
python3 execution/setup_docker_environment.py \
  --project-name my-cms \
  --mysql-password secret \
  --mysql-database cms_db
```

3. **Install Laravel dependencies**
```bash
docker-compose exec laravel composer install
```

4. **Install Next.js dependencies**
```bash
docker-compose exec nextjs npm install
```

5. **Run migrations and seed data**
```bash
docker-compose exec laravel php artisan migrate:fresh --seed
```

6. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/v1
- Admin Panel: http://localhost:8000/admin
- Mailhog: http://localhost:8025

### Default Admin Credentials
- Email: `admin@admin.com`
- Password: `password`

## 📁 Project Structure

```
cms-system/
├── backend/                    # Laravel API
│   ├── app/
│   │   ├── Models/            # Eloquent models
│   │   ├── Http/
│   │   │   ├── Controllers/   # API controllers
│   │   │   └── Resources/     # JSON resources
│   │   └── Filament/          # Admin panel
│   ├── database/
│   │   ├── migrations/        # Database schema
│   │   └── seeders/           # Demo data
│   └── Dockerfile
├── frontend/                   # Next.js frontend
│   ├── app/                   # App Router
│   │   ├── (shop)/           # Shop theme
│   │   ├── (travel)/         # Travel theme
│   │   ├── (restaurant)/     # Restaurant theme
│   │   └── (corporate)/      # Corporate theme
│   ├── components/
│   │   ├── shared/           # Shared components
│   │   └── themes/           # Theme-specific
│   ├── lib/                  # Utilities
│   └── Dockerfile
├── execution/                  # Python automation scripts
├── directives/                 # Markdown SOPs
├── docs/                       # Documentation
├── docker-compose.yml         # Container orchestration
├── AGENTS.md                  # AI agent instructions
├── GEMINI.md                  # Gemini-specific guide
└── README.md                  # This file
```

## 🤖 AI Agent System

This project uses a 3-layer architecture for AI-assisted development:

1. **Directives** (`directives/`): What to do (Markdown SOPs)
2. **Orchestration** (AI): Decision making and routing
3. **Execution** (`execution/`): Python scripts that do the work

### Using the Agent System

1. Read `AGENTS.md` for comprehensive instructions
2. Read `GEMINI.md` if using Google AI Studio
3. Use directives to understand each component
4. Run execution scripts to automate tasks

### Example: Adding a New Feature

```bash
# 1. Create a directive
directives/add_wishlist_feature.md

# 2. Let AI orchestrate the implementation
# AI reads directive → Calls execution scripts → Updates codebase

# 3. AI updates directive with learnings
```

## 🛠️ Development Workflow

### Starting the development environment
```bash
docker-compose up -d
```

### Stopping the environment
```bash
docker-compose down
```

### Viewing logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f laravel
docker-compose logs -f nextjs
```

### Accessing container shell
```bash
docker-compose exec laravel sh
docker-compose exec nextjs sh
```

### Running Laravel commands
```bash
docker-compose exec laravel php artisan migrate
docker-compose exec laravel php artisan make:model Product
docker-compose exec laravel php artisan route:list
```

### Running Next.js commands
```bash
docker-compose exec nextjs npm run build
docker-compose exec nextjs npm run lint
```

## 🎨 Themes

The system supports multiple themes for different business types. Each theme has:

- Custom layout and navigation
- Unique components
- Theme-specific routing
- Optimized for the business type

### Switching Themes

Themes are route-based. Access different themes via:

- Shop: `http://localhost:3000/` (default)
- Travel: `http://localhost:3000/tours`
- Restaurant: `http://localhost:3000/menu`
- Corporate: `http://localhost:3000/services`

### Creating a New Theme

1. Create route group: `app/(theme-name)/`
2. Add theme-specific components: `components/themes/theme-name/`
3. Implement layout and pages
4. Connect to Laravel API

## 🔐 Security

- Environment variables stored in `.env` (never committed)
- API authentication via Laravel Sanctum
- CORS configured for frontend
- SQL injection prevention via Eloquent ORM
- XSS protection via React escaping
- File upload validation

## 🚢 Deployment

### Indonesian/Singapore Hosting Options

**Recommended providers:**
- Niagahoster (Indonesia)
- Dewaweb (Indonesia)
- DigitalOcean Singapore
- AWS Singapore (ap-southeast-1)

### Deployment Steps

1. **Build production images**
```bash
docker-compose -f docker-compose.prod.yml build
```

2. **Push to registry**
```bash
docker tag cms-laravel your-registry/cms-laravel:latest
docker push your-registry/cms-laravel:latest
```

3. **Deploy to server**
```bash
# On server
docker-compose -f docker-compose.prod.yml up -d
```

4. **Run migrations**
```bash
docker-compose exec laravel php artisan migrate --force
```

5. **Clear caches**
```bash
docker-compose exec laravel php artisan optimize:clear
```

## 📊 Performance

### Target Metrics
- API response time: <200ms
- Page load time: <2 seconds
- Lighthouse score: 90+
- Core Web Vitals: All green

### Optimization Techniques
- Next.js ISR for static generation
- Laravel query optimization with eager loading
- Redis caching for API responses
- Image optimization with Next/Image
- CDN integration (Cloudflare)

## 🧪 Testing

### Backend Tests (Laravel)
```bash
docker-compose exec laravel php artisan test
```

### Frontend Tests (Next.js)
```bash
docker-compose exec nextjs npm run test
```

### E2E Tests
```bash
docker-compose exec nextjs npm run test:e2e
```

## 📝 API Documentation

API endpoints follow REST conventions:

### Shop Endpoints
- `GET /api/v1/shop/products` - List products
- `GET /api/v1/shop/products/{slug}` - Get product
- `GET /api/v1/shop/categories` - List categories

### Travel Endpoints
- `GET /api/v1/travel/tours` - List tour packages
- `GET /api/v1/travel/tours/{slug}` - Get tour details

### Restaurant Endpoints
- `GET /api/v1/restaurant/menu` - List menu items
- `POST /api/v1/restaurant/reservations` - Create reservation

### Corporate Endpoints
- `GET /api/v1/corporate/services` - List services
- `GET /api/v1/corporate/portfolio` - List portfolio items

Full API documentation available at: http://localhost:8000/api/documentation

## 🐛 Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs [service-name]

# Rebuild container
docker-compose build --no-cache [service-name]
```

### Database connection failed
```bash
# Verify MySQL is running
docker-compose ps mysql

# Check MySQL logs
docker-compose logs mysql

# Ensure correct credentials in .env
```

### Port already in use
```bash
# Find process using port
lsof -i :3000

# Kill process or change port in docker-compose.yml
```

### Permission denied errors
```bash
# Fix Laravel storage permissions
docker-compose exec laravel chmod -R 775 storage bootstrap/cache
```

## 📚 Documentation

- [Setup Docker Environment](directives/setup_docker_environment.md)
- [Setup Laravel Backend](directives/setup_laravel_backend.md)
- [Generate Next.js Frontend](directives/generate_nextjs_frontend.md)
- [AI Agent Instructions](AGENTS.md)
- [Gemini Guide](GEMINI.md)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 💬 Support

For issues and questions:
- GitHub Issues: [repository-url]/issues
- Email: support@example.com

## 🙏 Acknowledgments

- Laravel Framework
- Next.js Framework
- Laravel Filament
- Tailwind CSS
- Docker

---

**Built with ❤️ for Indonesian and Southeast Asian businesses**
