# 📁 CMS System - Complete Folder Structure Guide

## 🗂️ Root Level Files (Top Directory)

These files should be in the **ROOT** of your project:

```
cms-system/                          ← Your main project folder
├── AGENTS.md                        ← Main agent instructions (ROOT)
├── GEMINI.md                        ← Gemini-specific guide (ROOT)
├── README.md                        ← Project documentation (ROOT)
├── .env.example                     ← Environment template (ROOT)
├── .gitignore                       ← Git ignore rules (ROOT)
├── docker-compose.yml               ← Main Docker orchestration (ROOT) *to be created
└── docker-compose.prod.yml          ← Production Docker config (ROOT) *to be created
```

## 📂 Folder Structure

```
cms-system/
│
├── 📄 AGENTS.md                     ← ROOT level
├── 📄 GEMINI.md                     ← ROOT level
├── 📄 README.md                     ← ROOT level
├── 📄 .env.example                  ← ROOT level
├── 📄 .gitignore                    ← ROOT level
│
├── 📁 directives/                   ← Folder for all directive files
│   ├── setup_docker_environment.md
│   ├── setup_laravel_backend.md
│   ├── generate_nextjs_frontend.md
│   ├── optimize_seo.md
│   └── deploy_production.md
│
├── 📁 execution/                    ← Folder for Python automation scripts
│   ├── setup_docker_environment.py
│   ├── setup_laravel_backend.py    *to be created
│   ├── setup_nextjs_frontend.py    *to be created
│   └── optimize_seo.py              *to be created
│
├── 📁 backend/                      ← Laravel application folder
│   ├── app/
│   │   ├── Models/
│   │   ├── Http/
│   │   │   ├── Controllers/
│   │   │   └── Resources/
│   │   ├── Services/
│   │   └── Filament/
│   ├── database/
│   │   ├── migrations/
│   │   └── seeders/
│   ├── routes/
│   │   └── api.php
│   ├── config/
│   ├── storage/
│   ├── public/
│   ├── docker/
│   │   └── nginx.conf
│   ├── Dockerfile                   ← Laravel Dockerfile
│   ├── Dockerfile.prod              ← Production Dockerfile
│   ├── .env                         ← Laravel environment (created by script)
│   ├── .env.example
│   ├── .dockerignore
│   ├── composer.json
│   └── artisan
│
├── 📁 frontend/                     ← Next.js application folder
│   ├── app/
│   │   ├── (shop)/                  ← Shop theme
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   └── products/
│   │   ├── (travel)/                ← Travel theme
│   │   ├── (restaurant)/            ← Restaurant theme
│   │   ├── (corporate)/             ← Corporate theme
│   │   ├── layout.tsx               ← Root layout
│   │   └── not-found.tsx
│   ├── components/
│   │   ├── shared/
│   │   └── themes/
│   │       ├── shop/
│   │       ├── travel/
│   │       ├── restaurant/
│   │       └── corporate/
│   ├── lib/
│   │   ├── api.ts
│   │   ├── seo.ts
│   │   └── utils.ts
│   ├── types/
│   │   └── index.ts
│   ├── public/
│   │   ├── images/
│   │   └── fonts/
│   ├── Dockerfile                   ← Next.js Dockerfile
│   ├── Dockerfile.prod              ← Production Dockerfile
│   ├── .env.local                   ← Next.js environment (created by script)
│   ├── .env.example
│   ├── .dockerignore
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── package.json
│   └── tsconfig.json
│
├── 📁 docs/                         ← Documentation folder
│   ├── architecture.md
│   ├── api-reference.md
│   └── deployment-guide.md
│
├── 📁 .tmp/                         ← Temporary files (auto-generated, git-ignored)
│   ├── scaffolds/
│   ├── test-data/
│   └── build-artifacts/
│
└── 📁 scripts/                      ← Helper scripts (optional)
    ├── backup.sh
    └── deploy.sh
```

## 📍 File Placement Summary

### ROOT LEVEL (cms-system/)
- `AGENTS.md` ✓
- `GEMINI.md` ✓
- `README.md` ✓
- `.env.example` ✓
- `.gitignore` ✓
- `docker-compose.yml` (to create)
- `docker-compose.prod.yml` (to create)

### INSIDE directives/ FOLDER
- `setup_docker_environment.md` ✓
- `setup_laravel_backend.md` ✓
- `generate_nextjs_frontend.md` ✓
- `optimize_seo.md` ✓
- `deploy_production.md` ✓

### INSIDE execution/ FOLDER
- `setup_docker_environment.py` ✓
- `setup_laravel_backend.py` (to create)
- `setup_nextjs_frontend.py` (to create)
- `optimize_seo.py` (to create)

### INSIDE backend/ FOLDER
All Laravel files including:
- `Dockerfile`
- `composer.json`
- `artisan`
- `app/`, `database/`, `routes/`, etc.

### INSIDE frontend/ FOLDER
All Next.js files including:
- `Dockerfile`
- `package.json`
- `next.config.js`
- `app/`, `components/`, `lib/`, etc.

### INSIDE docs/ FOLDER
- Additional documentation
- Architecture diagrams
- API references

### INSIDE .tmp/ FOLDER
- Temporary files (auto-generated)
- Never committed to git
- Can be deleted anytime

## 🎯 How to Organize Your Project

### Option 1: Manual Setup (Recommended for Learning)

1. **Create main project folder:**
```bash
mkdir cms-system
cd cms-system
```

2. **Place root files:**
```bash
# Copy AGENTS.md, GEMINI.md, README.md, .env.example, .gitignore to root
```

3. **Create folder structure:**
```bash
mkdir -p directives execution backend frontend docs .tmp scripts
```

4. **Move files to correct folders:**
```bash
# Move all directive .md files to directives/
mv setup_docker_environment.md directives/
mv setup_laravel_backend.md directives/
# etc...

# Move all .py files to execution/
mv setup_docker_environment.py execution/
# etc...
```

### Option 2: Automated Setup (Recommended for Speed)

Use the provided execution script:
```bash
cd cms-system
python3 execution/setup_docker_environment.py
```

This will automatically create:
- `backend/` folder with Dockerfile
- `frontend/` folder with Dockerfile
- `docker-compose.yml` in root
- `.env` files in correct locations

## 🔍 Quick Verification

After setup, your structure should look like:

```bash
cms-system/
├── AGENTS.md                    ✓ (in root)
├── GEMINI.md                    ✓ (in root)
├── README.md                    ✓ (in root)
├── .env.example                 ✓ (in root)
├── .gitignore                   ✓ (in root)
├── docker-compose.yml           ✓ (in root, created by script)
├── directives/                  ✓ (folder)
│   └── *.md files               ✓ (5 directive files)
├── execution/                   ✓ (folder)
│   └── *.py files               ✓ (Python scripts)
├── backend/                     ✓ (folder, created by script)
├── frontend/                    ✓ (folder, created by script)
└── docs/                        ✓ (folder)
```

## 🚨 Common Mistakes to Avoid

❌ **DON'T put directives/ in backend/**
```
backend/directives/  ← WRONG!
```

✅ **DO put directives/ in root:**
```
cms-system/directives/  ← CORRECT!
```

❌ **DON'T put AGENTS.md inside any folder**
```
backend/AGENTS.md  ← WRONG!
docs/AGENTS.md     ← WRONG!
```

✅ **DO put AGENTS.md in root:**
```
cms-system/AGENTS.md  ← CORRECT!
```

❌ **DON'T mix execution scripts with backend code**
```
backend/execution/  ← WRONG!
```

✅ **DO keep execution/ separate in root:**
```
cms-system/execution/  ← CORRECT!
```

## 📦 What Gets Git Committed

### ✅ COMMIT THESE:
- `AGENTS.md`, `GEMINI.md`, `README.md`
- All files in `directives/`
- All files in `execution/`
- All files in `backend/` (except vendor/, .env, logs)
- All files in `frontend/` (except node_modules/, .next/, .env.local)
- `docker-compose.yml`, `docker-compose.prod.yml`
- `.env.example`, `.gitignore`

### ❌ DON'T COMMIT THESE:
- `.env` files (use `.env.example` instead)
- `node_modules/`, `vendor/`
- `.next/`, `storage/logs/`
- `.tmp/` folder (temporary files)
- Database files, credential files

## 🎓 Understanding the Structure

### Why This Structure?

1. **Root level (AGENTS.md, GEMINI.md, README.md)**
   - First files AI and developers see
   - Project-wide instructions
   - Easy to find

2. **directives/ folder**
   - All SOPs in one place
   - Easy to browse and update
   - Organized by feature

3. **execution/ folder**
   - All automation scripts together
   - Python environment isolated
   - Easy to execute

4. **backend/ and frontend/ folders**
   - Separate concerns
   - Independent Docker containers
   - Can be developed separately

5. **.tmp/ folder**
   - Keeps root clean
   - Safe to delete
   - Not in version control

## 🔄 Development Workflow

```bash
# 1. Start in root
cd cms-system/

# 2. Read agent instructions
cat AGENTS.md

# 3. Check available directives
ls directives/

# 4. Run execution script
python3 execution/setup_docker_environment.py

# 5. Work in backend
cd backend/
composer install

# 6. Work in frontend
cd ../frontend/
npm install

# 7. Back to root for Docker commands
cd ..
docker compose up -d
```

## ✅ Final Checklist

Before starting development, verify:

- [ ] AGENTS.md is in root (not in any subfolder)
- [ ] GEMINI.md is in root (not in any subfolder)
- [ ] README.md is in root (not in any subfolder)
- [ ] directives/ folder contains 5 .md files
- [ ] execution/ folder contains .py scripts
- [ ] backend/ folder exists (empty is OK, will be populated)
- [ ] frontend/ folder exists (empty is OK, will be populated)
- [ ] .gitignore is in root
- [ ] .env.example is in root (NOT .env yet)

---

**Now you're ready to start building!** 🚀

The execution scripts will automatically create the backend/, frontend/, and other folders with the correct structure when you run them.