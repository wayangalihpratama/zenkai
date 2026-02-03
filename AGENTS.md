# Agent Instructions - Modular CMS System
> This file is mirrored across CLAUDE.md, AGENTS.md, and GEMINI.md so the same instructions load in any AI environment.

## Project Overview
You are building a **modular, headless CMS system** with:
- **Backend:** Laravel 11+ (API-first architecture)
- **Frontend:** Next.js 14+ (App Router, SEO-optimized)
- **Database:** MySQL 8.0+
- **Admin Panel:** Laravel Filament 3.x (preferred) or Laravel Nova
- **Deployment:** Dockerized for local development, deployable to Indonesian/Singapore hosting
- **Target Users:** Shops, travel agents, restaurants, corporate websites

## The 3-Layer Architecture

LLMs are probabilistic, whereas most business logic is deterministic and requires consistency. This system fixes that mismatch.

### Layer 1: Directive (What to do)
- SOPs written in Markdown, live in `directives/`
- Define the goals, inputs, tools/scripts to use, outputs, and edge cases
- Natural language instructions for each major task
- Updated continuously as you learn constraints and optimizations

### Layer 2: Orchestration (Decision making)
- **This is you.** Your job: intelligent routing and decision-making.
- Read directives, call execution tools in the right order, handle errors
- Ask for clarification when requirements are ambiguous
- Update directives with learnings from errors and edge cases
- You're the glue between intent and execution

**Critical Rule:** You don't manually code large features—you read the directive (e.g., `directives/setup_laravel_backend.md`), determine inputs/outputs, then run the appropriate execution script (e.g., `execution/setup_laravel.py`).

### Layer 3: Execution (Doing the work)
- Deterministic Python scripts in `execution/`
- Handle Docker operations, API calls, file generation, database migrations
- Environment variables stored in `.env`
- Reliable, testable, fast, well-commented
- Scripts are idempotent where possible

**Why this works:** 90% accuracy per step = 59% success over 5 steps. By pushing complexity into deterministic code, you focus on decision-making, not implementation details.

## Operating Principles

### 1. Check for tools first
Before writing new code, check `execution/` directory per your directive. Only create new scripts if none exist or existing ones don't fit the use case.

### 2. Docker-first development
- All development happens in Docker containers
- `docker-compose.yml` defines the full stack
- Never install dependencies on host machine
- Scripts should work inside containers

### 3. Self-anneal when things break
When errors occur:
1. Read error message and stack trace carefully
2. Identify root cause (API limit? Docker network? Missing env var?)
3. Fix the script and test again (unless it uses paid resources—ask user first)
4. Update the directive with what you learned
5. System is now stronger

**Example:** You hit a MySQL connection error → investigate `docker-compose.yml` → find network misconfiguration → fix network settings → update `directives/setup_docker_environment.md` with common networking issues.

### 4. Update directives as you learn
Directives are living documents. When you discover:
- API constraints or rate limits
- Better architectural approaches
- Common errors and their solutions
- Timing expectations or performance bottlenecks

**Update the directive immediately.** But don't create or overwrite directives without asking unless explicitly told to.

### 5. SEO is non-negotiable
Every frontend output must be:
- Server-side rendered (SSR) or statically generated (SSG)
- Have proper meta tags (Open Graph, Twitter Cards)
- Include structured data (JSON-LD schema)
- Pass Core Web Vitals
- Mobile-first responsive

### 6. Security-first approach
- Never commit secrets (`.env`, `token.json`, credentials)
- Validate all inputs in execution scripts
- Use parameterized queries for database operations
- Follow Laravel security best practices
- Docker containers run as non-root users where possible

## System Architecture

### Backend Structure (Laravel)
```
backend/
├── app/
│   ├── Models/           # Eloquent models (polymorphic for multi-tenant)
│   ├── Http/
│   │   ├── Controllers/  # API controllers (versioned: /api/v1/)
│   │   └── Resources/    # API resources for consistent JSON responses
│   ├── Services/         # Business logic layer
│   └── Filament/         # Admin panel resources
├── database/
│   ├── migrations/       # Database schema
│   └── seeders/          # Demo data for each website type
├── routes/
│   └── api.php          # API routes
└── docker/
    └── Dockerfile       # Laravel container
```

### Frontend Structure (Next.js)
```
frontend/
├── app/                 # Next.js App Router
│   ├── (shop)/         # Shop theme routes
│   ├── (travel)/       # Travel agent theme routes
│   ├── (restaurant)/   # Restaurant theme routes
│   └── (corporate)/    # Corporate theme routes
├── components/
│   ├── shared/         # Shared components across themes
│   └── themes/         # Theme-specific components
├── lib/
│   ├── api.ts          # API client for Laravel backend
│   └── seo.ts          # SEO utilities (metadata, schema)
└── public/             # Static assets
```

### Docker Configuration
```
.
├── docker-compose.yml          # Multi-container orchestration
├── docker-compose.dev.yml      # Development overrides
├── docker-compose.prod.yml     # Production overrides
├── .env.example                # Environment template
└── .dockerignore               # Exclude from build context
```

## File Organization

### Deliverables vs Intermediates

**Deliverables:** Production code, Docker images, deployment configs
- `backend/` - Laravel application
- `frontend/` - Next.js application
- `docker-compose.yml` - Container orchestration
- `docs/` - System documentation

**Intermediates:** Temporary files during processing
- `.tmp/` - Scaffolding outputs, test data, build artifacts
- `logs/` - Docker and application logs (ignored in git)

### Directory Structure
```
cms-system/
├── .tmp/                       # Temporary files (never commit)
├── backend/                    # Laravel API
├── frontend/                   # Next.js frontend
├── execution/                  # Python automation scripts
├── directives/                 # Markdown SOPs
├── docs/                       # System documentation
├── .env.example               # Environment template
├── docker-compose.yml         # Docker orchestration
├── AGENTS.md                  # This file
├── GEMINI.md                  # Gemini-specific instructions
└── README.md                  # Quick start guide
```

**Key principle:** All development and testing happens in Docker. The system should work identically on any machine with Docker installed.

## Feature Requirements by Website Type

### 1. Shop (E-commerce)
**Must-have features:**
- Product catalog with categories and tags
- Shopping cart and checkout flow
- Payment integration (Midtrans for Indonesia)
- Order management and tracking
- Inventory management
- Customer accounts and order history
- Product search and filtering
- Multi-currency support (IDR, SGD, USD)

**SEO requirements:**
- Product schema (JSON-LD)
- Dynamic sitemaps
- Optimized product images
- Rich snippets for pricing and availability

### 2. Travel Agent
**Must-have features:**
- Tour packages with itineraries
- Booking system with calendar availability
- Multi-day trip planning
- Customer inquiry forms
- Gallery with destination photos
- Testimonials and reviews
- Multi-language support (EN, ID)
- Payment and deposit management

**SEO requirements:**
- Trip schema (JSON-LD)
- Location-based SEO
- Blog for destination guides
- Image optimization for galleries

### 3. Restaurant
**Must-have features:**
- Digital menu with categories
- Table reservation system
- Online ordering (delivery/pickup)
- Gallery for food photos
- Operating hours and location
- Special offers and promotions
- Multi-location support
- Integration with food delivery platforms (GrabFood, GoFood)

**SEO requirements:**
- Restaurant schema (JSON-LD)
- Local business markup
- Menu item schema
- Google My Business integration

### 4. Corporate Website
**Must-have features:**
- About us / Team profiles
- Services/Products showcase
- Portfolio/Case studies
- Blog/News section
- Contact forms
- Career/Job listings
- Multi-page structure
- Download center for brochures/PDFs

**SEO requirements:**
- Organization schema (JSON-LD)
- Breadcrumb navigation
- Blog post schema
- FAQ schema

## Deployment Strategy

### Local Development (Docker)
- `docker compose up` starts entire stack
- Hot reload for both Laravel and Next.js
- MySQL with persistent volumes
- Mailhog for email testing

### Indonesian/Singapore Hosting
**Recommended providers:**
- Niagahoster (Indonesia) - cPanel with Docker support
- Dewaweb (Indonesia) - VPS options
- DigitalOcean Singapore - Droplets
- AWS Singapore (ap-southeast-1)

**Deployment requirements:**
- Docker or Docker Swarm support
- Minimum 2GB RAM
- SSL certificate (Let's Encrypt)
- CDN integration (Cloudflare)

## Self-Annealing Loop

When something breaks, follow this process:

1. **Identify the error**
   - Read stack trace carefully
   - Check Docker logs: `docker-compose logs [service]`
   - Review recent changes

2. **Fix it**
   - Update execution script or configuration
   - Test in isolated environment first
   - Verify fix works in full stack

3. **Update the tool**
   - Add error handling for this case
   - Improve logging for debugging
   - Make script more resilient

4. **Document the learning**
   - Update relevant directive with:
     - What went wrong
     - Root cause
     - How to prevent it
     - Alternative approaches

5. **System is now stronger**
   - Future runs avoid this error
   - Knowledge is preserved
   - Team learns from mistakes

## Working with Gemini

Since you're using Google AI Studio with Gemini:

1. **Use the GEMINI.md file** for Gemini-specific optimizations
2. **Token management:** Gemini has large context windows (1M+ tokens for Gemini 1.5 Pro)
3. **Code execution:** Gemini can execute Python directly—use this for quick tests
4. **Multimodal:** Can analyze UI screenshots, database diagrams, architecture drawings

## Summary

You are the **orchestration layer** between human intent (directives) and deterministic execution (Python scripts). Your responsibilities:

✅ Read directives to understand requirements
✅ Call execution scripts in the right order
✅ Handle errors gracefully and learn from them
✅ Update directives with new knowledge
✅ Make intelligent decisions about architecture
✅ Ensure SEO, security, and performance standards

❌ Don't manually code large features
❌ Don't skip Docker—everything runs in containers
❌ Don't commit secrets or temporary files
❌ Don't ignore SEO requirements
❌ Don't proceed without confirming breaking changes

**Be pragmatic. Be reliable. Self-anneal. Build a CMS that scales.**
