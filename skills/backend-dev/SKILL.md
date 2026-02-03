---
name: backend-dev
description: comprehensive guide for Laravel backend development, including API design, database modeling, and Filament admin panel integration. Use when building or modifying backend logic, controllers, models, migrations, or admin resources.
license: Complete terms in LICENSE.txt
---

# Laravel Backend Development

This skill guides the development of robust, scalable, and maintainable Laravel backends.

## 🏗 Architectural Principles

### 1. Service-Oriented / Action-Based Architecture
- **Avoid "Fat Controllers"**: Controllers should handle request parsing and response formatting ONLY.
- **Business Logic**: Encapsulate logic in **Service Classes** (for shared logic) or **Action Classes** (for single-purpose operations).
- **Filament Resources**: Use Filament resources for all admin CRUD operations.

### 2. SOLID Principles
- **Single Responsibility**: Each class should have one reason to change.
- **Dependency Injection**: Inject dependencies (Repositories, Services) rather than using Facades deep in logic when possible, improving testability.

## 🛠 Coding Standards

### Models & Database
- **Strict Typing**: Use strict types in all methods.
- **Eloquent**: Use relationships, scopes, and accessors effectively.
- **Mass Assignment**: Always define `$fillable` or `$guarded`.
- **Migrations**: Always use constrained foreign keys (`foreignId()->constrained()->cascadeOnDelete()`).

### APIs (Laravel 11+)
- **API Resources**: Always use `JsonResource` to transform models into JSON responses. Never return Eloquent models directly.
- **Form Requests**: Use strict `FormRequest` classes for validation. Do not validate in controllers.
- **Versioning**: Prefix API routes with `v1`, `v2`, etc.

## 📦 Filament Admin Panel
- **Resources**: Create resources for all primary entities (`php artisan make:filament-resource`).
- **Forms**: Use the `Form` builder for clean, schema-based definitions.
- **Tables**: Use the `Table` builder for data display.

## 🧪 Testing
- **PEST / PHPUnit**: Write Feature tests for all API endpoints.
- **Happy Path & Edge Cases**: Test valid inputs AND invalid inputs (422 validation errors).

## 🚀 Workflow

1. **Plan**: Define the data model and API contract.
2. **Migration**: Create and run migrations.
3. **Model**: Define model relationships and casts.
4. **Filament**: Generate admin resource (if managed by admin).
5. **API**: Create Controller, Form Request, and API Resource.
6. **Routes**: Register routes in `api.php`.
7. **Test**: Verify with tests.

## Common Commands

```bash
# Create Model + Migration + Factory + Seeder + Controller + Requests
php artisan make:model Product -mfs -c -R

# Create Filament Resource
php artisan make:filament-resource Product

# Run Tests
php artisan test
```
