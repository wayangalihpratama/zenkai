# Directive: Setup Laravel Backend

## Goal
Create a production-ready Laravel 11 API backend with Filament admin panel, polymorphic database structure for multi-tenant CMS, and complete CRUD functionality for all website types (Shop, Travel, Restaurant, Corporate).

## Prerequisites
- Docker environment running (`directives/setup_docker_environment.md` completed)
- MySQL database accessible
- Composer available in Laravel container

## Inputs
- `website_type` (enum): "shop" | "travel" | "restaurant" | "corporate" | "all"
- `admin_panel` (enum): "filament" | "nova" (default: "filament")
- `enable_features` (array): List of features to enable per website type

## Execution Tool
**Script:** `execution/setup_laravel_backend.py`

## Process Flow

### 1. Initialize Laravel Project
Inside Laravel container:
```bash
composer create-project laravel/laravel:^11.0 .
composer require laravel/sanctum
composer require spatie/laravel-permission
composer require spatie/laravel-medialibrary
composer require spatie/laravel-sluggable
```

### 2. Install Admin Panel

**Option A: Filament (Recommended)**
```bash
composer require filament/filament:"^3.0"
php artisan filament:install --panels
```

**Option B: Laravel Nova**
```bash
composer require laravel/nova
php artisan nova:install
```

### 3. Create Database Architecture

Design polymorphic structure to support multiple website types:

**Core Models:**
- `Website` - Main website entity (type: shop/travel/restaurant/corporate)
- `Page` - Dynamic pages
- `Media` - File uploads (using Spatie Media Library)
- `Setting` - Site settings (JSON storage)

**Shop Models:**
- `Product`
- `Category`
- `Order`
- `OrderItem`
- `Cart`
- `Customer`
- `PaymentMethod`

**Travel Models:**
- `TourPackage`
- `Itinerary`
- `Booking`
- `Destination`
- `Review`

**Restaurant Models:**
- `MenuItem`
- `MenuCategory`
- `Reservation`
- `Location`
- `SpecialOffer`

**Corporate Models:**
- `Service`
- `Portfolio`
- `TeamMember`
- `JobPosting`
- `Inquiry`

### 4. Generate Migrations

Create migration files for all models with proper relationships:

**Example: Product Migration**
```php
Schema::create('products', function (Blueprint $table) {
    $table->id();
    $table->foreignId('website_id')->constrained()->cascadeOnDelete();
    $table->foreignId('category_id')->nullable()->constrained()->nullOnDelete();
    $table->string('name');
    $table->string('slug')->unique();
    $table->text('description')->nullable();
    $table->decimal('price', 12, 2);
    $table->decimal('compare_at_price', 12, 2)->nullable();
    $table->integer('stock')->default(0);
    $table->string('sku')->unique()->nullable();
    $table->json('metadata')->nullable(); // For SEO, variants, etc.
    $table->boolean('is_active')->default(true);
    $table->timestamps();
    $table->softDeletes();
});
```

### 5. Create Eloquent Models

Generate models with:
- Relationships (BelongsTo, HasMany, MorphMany)
- Accessors/Mutators
- Query scopes
- Sluggable trait
- Media handling

**Example: Product Model**
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Spatie\MediaLibrary\HasMedia;
use Spatie\MediaLibrary\InteractsWithMedia;
use Spatie\Sluggable\HasSlug;
use Spatie\Sluggable\SlugOptions;

class Product extends Model implements HasMedia
{
    use SoftDeletes, InteractsWithMedia, HasSlug;

    protected $fillable = [
        'website_id', 'category_id', 'name', 'slug',
        'description', 'price', 'compare_at_price',
        'stock', 'sku', 'metadata', 'is_active'
    ];

    protected $casts = [
        'metadata' => 'array',
        'is_active' => 'boolean',
        'price' => 'decimal:2',
        'compare_at_price' => 'decimal:2'
    ];

    public function getSlugOptions(): SlugOptions
    {
        return SlugOptions::create()
            ->generateSlugsFrom('name')
            ->saveSlugsTo('slug');
    }

    public function website()
    {
        return $this->belongsTo(Website::class);
    }

    public function category()
    {
        return $this->belongsTo(Category::class);
    }

    public function orders()
    {
        return $this->belongsToMany(Order::class, 'order_items')
            ->withPivot('quantity', 'price');
    }

    public function registerMediaCollections(): void
    {
        $this->addMediaCollection('images')
            ->useDisk('public')
            ->registerMediaConversions(function (Media $media) {
                $this->addMediaConversion('thumb')
                    ->width(300)
                    ->height(300);
                $this->addMediaConversion('preview')
                    ->width(800)
                    ->height(800);
            });
    }
}
```

### 6. Create API Controllers

Generate resourceful controllers for each model:

**Structure:**
```
app/Http/Controllers/Api/V1/
├── Shop/
│   ├── ProductController.php
│   ├── CategoryController.php
│   └── OrderController.php
├── Travel/
│   ├── TourPackageController.php
│   └── BookingController.php
├── Restaurant/
│   ├── MenuItemController.php
│   └── ReservationController.php
└── Corporate/
    ├── ServiceController.php
    └── PortfolioController.php
```

**Example: ProductController**
```php
<?php

namespace App\Http\Controllers\Api\V1\Shop;

use App\Http\Controllers\Controller;
use App\Http\Resources\ProductResource;
use App\Models\Product;
use Illuminate\Http\Request;

class ProductController extends Controller
{
    public function index(Request $request)
    {
        $query = Product::with(['category', 'media'])
            ->where('website_id', $request->website_id)
            ->where('is_active', true);

        if ($request->has('category_id')) {
            $query->where('category_id', $request->category_id);
        }

        if ($request->has('search')) {
            $query->where('name', 'like', '%' . $request->search . '%');
        }

        $products = $query->paginate($request->get('per_page', 15));

        return ProductResource::collection($products);
    }

    public function show(string $slug)
    {
        $product = Product::with(['category', 'media'])
            ->where('slug', $slug)
            ->firstOrFail();

        return new ProductResource($product);
    }
}
```

### 7. Create API Resources

Generate JSON API resources for consistent response format:

**Example: ProductResource**
```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class ProductResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'slug' => $this->slug,
            'description' => $this->description,
            'price' => [
                'amount' => $this->price,
                'formatted' => 'Rp ' . number_format($this->price, 0, ',', '.')
            ],
            'compare_at_price' => $this->compare_at_price ? [
                'amount' => $this->compare_at_price,
                'formatted' => 'Rp ' . number_format($this->compare_at_price, 0, ',', '.')
            ] : null,
            'stock' => $this->stock,
            'in_stock' => $this->stock > 0,
            'sku' => $this->sku,
            'images' => $this->getMedia('images')->map(function ($media) {
                return [
                    'id' => $media->id,
                    'url' => $media->getUrl(),
                    'thumb' => $media->getUrl('thumb'),
                    'preview' => $media->getUrl('preview'),
                    'alt' => $media->getCustomProperty('alt') ?? $this->name
                ];
            }),
            'category' => new CategoryResource($this->whenLoaded('category')),
            'metadata' => $this->metadata,
            'created_at' => $this->created_at->toIso8601String(),
            'updated_at' => $this->updated_at->toIso8601String()
        ];
    }
}
```

### 8. Setup API Routes

Define versioned API routes:

**routes/api.php:**
```php
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\V1;

Route::prefix('v1')->group(function () {

    // Health check
    Route::get('/health', fn() => response()->json(['status' => 'ok']));

    // Shop endpoints
    Route::prefix('shop')->group(function () {
        Route::get('/products', [V1\Shop\ProductController::class, 'index']);
        Route::get('/products/{slug}', [V1\Shop\ProductController::class, 'show']);
        Route::get('/categories', [V1\Shop\CategoryController::class, 'index']);
    });

    // Travel endpoints
    Route::prefix('travel')->group(function () {
        Route::get('/tours', [V1\Travel\TourPackageController::class, 'index']);
        Route::get('/tours/{slug}', [V1\Travel\TourPackageController::class, 'show']);
    });

    // Restaurant endpoints
    Route::prefix('restaurant')->group(function () {
        Route::get('/menu', [V1\Restaurant\MenuItemController::class, 'index']);
        Route::post('/reservations', [V1\Restaurant\ReservationController::class, 'store']);
    });

    // Corporate endpoints
    Route::prefix('corporate')->group(function () {
        Route::get('/services', [V1\Corporate\ServiceController::class, 'index']);
        Route::get('/portfolio', [V1\Corporate\PortfolioController::class, 'index']);
    });
});
```

### 9. Setup Filament Admin Panel

Generate Filament resources for all models:

```bash
php artisan make:filament-resource Product --generate
php artisan make:filament-resource TourPackage --generate
php artisan make:filament-resource MenuItem --generate
```

Customize Filament resources with:
- Form fields (TextInput, Textarea, FileUpload, etc.)
- Table columns
- Filters
- Actions
- Bulk actions

### 10. Configure CORS

**config/cors.php:**
```php
return [
    'paths' => ['api/*'],
    'allowed_methods' => ['*'],
    'allowed_origins' => ['http://localhost:3000'],
    'allowed_origins_patterns' => [],
    'allowed_headers' => ['*'],
    'exposed_headers' => [],
    'max_age' => 0,
    'supports_credentials' => false,
];
```

### 11. Create Seeders

Generate demo data for each website type:

```bash
php artisan make:seeder ShopSeeder
php artisan make:seeder TravelSeeder
php artisan make:seeder RestaurantSeeder
php artisan make:seeder CorporateSeeder
```

### 12. Run Migrations and Seeds

```bash
php artisan migrate:fresh
php artisan db:seed
```

## Expected Outputs

### Success
- Laravel application running at http://localhost:8000
- API endpoints responding correctly
- Filament admin accessible at http://localhost:8000/admin
- Database tables created with relationships
- Demo data seeded

**API Response Example:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Premium Widget",
      "slug": "premium-widget",
      "price": {
        "amount": 150000,
        "formatted": "Rp 150.000"
      },
      "images": [
        {
          "url": "http://localhost:8000/storage/products/1/image.jpg",
          "thumb": "http://localhost:8000/storage/products/1/conversions/image-thumb.jpg"
        }
      ]
    }
  ],
  "links": {...},
  "meta": {...}
}
```

### Failure Scenarios

**1. Migration Fails**
- Error: "Syntax error or access violation"
- Cause: Invalid column definition or foreign key constraint
- Solution: Review migration file, check table order
- Update directive: Document migration dependency order

**2. Composer Memory Limit**
- Error: "Allowed memory size exhausted"
- Solution: `php -d memory_limit=-1 /usr/local/bin/composer install`
- Update directive: Add memory settings to Dockerfile

**3. Storage Permission Issues**
- Error: "failed to open stream: Permission denied"
- Solution: `chmod -R 775 storage bootstrap/cache`
- Update directive: Add permission setup to Docker entrypoint

**4. Filament Installation Conflict**
- Error: "Your requirements could not be resolved"
- Cause: Version conflicts with Laravel 11
- Solution: Use specific Filament version `composer require filament/filament:"^3.2"`
- Update directive: Document compatible versions

## Edge Cases

### Multi-Currency Support
- Store prices in cents (integer)
- Add `currency` column to Website model
- Format based on locale in API resources

### Multi-Language Content
- Use `spatie/laravel-translatable` for translatable fields
- Add `translations` JSON column
- API returns content based on `Accept-Language` header

### Soft Deletes
- All main models should use SoftDeletes
- API should not show soft-deleted records by default
- Admin can restore via Filament

## Testing Checklist

After running the script, verify:
- [ ] Laravel responds at http://localhost:8000
- [ ] API health endpoint returns 200
- [ ] Filament admin accessible (default: admin@admin.com / password)
- [ ] Can create product via Filament
- [ ] API returns products with images
- [ ] Relationships work (product → category)
- [ ] CORS allows requests from Next.js
- [ ] Pagination works correctly
- [ ] Search and filters functional

## Performance Expectations
- API response time: <200ms for paginated lists
- API response time: <100ms for single resource
- Database queries: N+1 prevented via eager loading
- Image upload: Optimized and converted automatically

## Updates to This Directive

### [2025-02-03] Initial creation
- Created comprehensive Laravel setup directive
- Defined all models and relationships
- Planned Filament integration

### Future improvements to track:
- Optimal eager loading strategies
- Caching strategies for frequently accessed data
- Rate limiting configurations
- Payment gateway integration details

---

**Remember:** Laravel is the source of truth. All business logic lives here. Next.js is just a presentation layer consuming this API.
