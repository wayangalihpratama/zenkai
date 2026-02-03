# Directive: Generate Next.js Frontend with Theme System

## Goal
Create a Next.js 14+ application with App Router, multiple interchangeable themes for different website types (Shop, Travel, Restaurant, Corporate), server-side rendering for SEO, and optimal Core Web Vitals performance.

## Prerequisites
- Docker environment running
- Laravel backend API accessible at http://localhost:8000
- Node.js 20+ available in Next.js container

## Inputs
- `website_type` (enum): "shop" | "travel" | "restaurant" | "corporate"
- `theme_style` (enum): "minimal" | "modern" | "bold" | "elegant"
- `primary_color` (string): Hex color code (e.g., "#3B82F6")
- `enable_features` (array): Features to enable for this theme

## Execution Tool
**Script:** `execution/setup_nextjs_frontend.py`

## Process Flow

### 1. Initialize Next.js Project

Inside Next.js container:
```bash
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir
npm install @tanstack/react-query axios zod react-hook-form
npm install -D @tailwindcss/typography @tailwindcss/forms
```

### 2. Configure Next.js

**next.config.js:**
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8000',
        pathname: '/storage/**',
      },
    ],
    formats: ['image/avif', 'image/webp'],
  },
  experimental: {
    optimizeCss: true,
  },
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
}

module.exports = nextConfig
```

### 3. Setup Project Structure

Create organized directory structure:

```
frontend/
├── app/
│   ├── (shop)/              # Shop theme route group
│   │   ├── layout.tsx       # Shop-specific layout
│   │   ├── page.tsx         # Home page
│   │   ├── products/
│   │   │   ├── page.tsx     # Product listing
│   │   │   └── [slug]/
│   │   │       └── page.tsx # Product detail
│   │   ├── cart/
│   │   │   └── page.tsx     # Shopping cart
│   │   └── checkout/
│   │       └── page.tsx     # Checkout flow
│   ├── (travel)/            # Travel theme route group
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── tours/
│   │   │   ├── page.tsx
│   │   │   └── [slug]/
│   │   │       └── page.tsx
│   │   └── booking/
│   │       └── page.tsx
│   ├── (restaurant)/        # Restaurant theme route group
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── menu/
│   │   │   └── page.tsx
│   │   └── reservation/
│   │       └── page.tsx
│   ├── (corporate)/         # Corporate theme route group
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── services/
│   │   ├── portfolio/
│   │   ├── about/
│   │   └── contact/
│   ├── api/                 # API routes (if needed)
│   │   └── revalidate/
│   │       └── route.ts
│   ├── layout.tsx           # Root layout
│   └── not-found.tsx        # 404 page
├── components/
│   ├── shared/              # Shared components
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── Navigation.tsx
│   │   └── SEO.tsx
│   └── themes/              # Theme-specific components
│       ├── shop/
│       │   ├── ProductCard.tsx
│       │   ├── ProductGrid.tsx
│       │   └── AddToCartButton.tsx
│       ├── travel/
│       │   ├── TourCard.tsx
│       │   └── BookingForm.tsx
│       ├── restaurant/
│       │   ├── MenuItem.tsx
│       │   └── ReservationForm.tsx
│       └── corporate/
│           ├── ServiceCard.tsx
│           └── PortfolioGrid.tsx
├── lib/
│   ├── api.ts               # API client
│   ├── seo.ts               # SEO utilities
│   ├── constants.ts         # App constants
│   └── utils.ts             # Helper functions
├── types/
│   └── index.ts             # TypeScript types
└── public/
    ├── images/
    ├── fonts/
    └── icons/
```

### 4. Create API Client

**lib/api.ts:**
```typescript
import axios from 'axios'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Product API
export const productApi = {
  getAll: async (params?: { category_id?: number; search?: string }) => {
    const { data } = await api.get('/shop/products', { params })
    return data
  },
  getBySlug: async (slug: string) => {
    const { data } = await api.get(`/shop/products/${slug}`)
    return data
  },
}

// Tour API
export const tourApi = {
  getAll: async () => {
    const { data } = await api.get('/travel/tours')
    return data
  },
  getBySlug: async (slug: string) => {
    const { data } = await api.get(`/travel/tours/${slug}`)
    return data
  },
}

// Menu API
export const menuApi = {
  getAll: async () => {
    const { data } = await api.get('/restaurant/menu')
    return data
  },
}

export default api
```

### 5. Setup TypeScript Types

**types/index.ts:**
```typescript
export interface Product {
  id: number
  name: string
  slug: string
  description: string
  price: {
    amount: number
    formatted: string
  }
  compare_at_price?: {
    amount: number
    formatted: string
  }
  stock: number
  in_stock: boolean
  sku: string
  images: ProductImage[]
  category?: Category
  metadata?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface ProductImage {
  id: number
  url: string
  thumb: string
  preview: string
  alt: string
}

export interface Category {
  id: number
  name: string
  slug: string
  description?: string
}

export interface TourPackage {
  id: number
  name: string
  slug: string
  description: string
  duration: number
  price: {
    amount: number
    formatted: string
  }
  images: ProductImage[]
  itinerary?: Itinerary[]
}

export interface MenuItem {
  id: number
  name: string
  description: string
  price: {
    amount: number
    formatted: string
  }
  category: string
  image?: ProductImage
  is_available: boolean
}
```

### 6. Create SEO Utilities

**lib/seo.ts:**
```typescript
import { Metadata } from 'next'

interface SEOProps {
  title: string
  description: string
  canonical?: string
  ogImage?: string
  noIndex?: boolean
}

export function generateSEO({
  title,
  description,
  canonical,
  ogImage,
  noIndex = false,
}: SEOProps): Metadata {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'
  
  return {
    title,
    description,
    robots: noIndex ? 'noindex,nofollow' : 'index,follow',
    alternates: {
      canonical: canonical || baseUrl,
    },
    openGraph: {
      title,
      description,
      url: canonical || baseUrl,
      siteName: 'CMS System',
      images: ogImage ? [
        {
          url: ogImage,
          width: 1200,
          height: 630,
          alt: title,
        },
      ] : [],
      type: 'website',
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
      images: ogImage ? [ogImage] : [],
    },
  }
}

export function generateProductSchema(product: any) {
  return {
    '@context': 'https://schema.org/',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.images.map((img: any) => img.url),
    sku: product.sku,
    offers: {
      '@type': 'Offer',
      url: `${process.env.NEXT_PUBLIC_SITE_URL}/products/${product.slug}`,
      priceCurrency: 'IDR',
      price: product.price.amount,
      availability: product.in_stock ? 'https://schema.org/InStock' : 'https://schema.org/OutOfStock',
    },
  }
}

export function generateRestaurantSchema(restaurant: any) {
  return {
    '@context': 'https://schema.org/',
    '@type': 'Restaurant',
    name: restaurant.name,
    description: restaurant.description,
    address: {
      '@type': 'PostalAddress',
      streetAddress: restaurant.address,
      addressLocality: restaurant.city,
      addressCountry: 'ID',
    },
    telephone: restaurant.phone,
    servesCuisine: restaurant.cuisine,
    priceRange: restaurant.price_range,
  }
}
```

### 7. Create Theme Layouts

**app/(shop)/layout.tsx:**
```typescript
import { Metadata } from 'next'
import Header from '@/components/themes/shop/Header'
import Footer from '@/components/themes/shop/Footer'

export const metadata: Metadata = {
  title: {
    default: 'Shop - Premium Products',
    template: '%s | Shop',
  },
  description: 'Browse our collection of premium products',
}

export default function ShopLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow">{children}</main>
      <Footer />
    </div>
  )
}
```

### 8. Create Product Listing Page (Shop Theme)

**app/(shop)/products/page.tsx:**
```typescript
import { Metadata } from 'next'
import { productApi } from '@/lib/api'
import { generateSEO } from '@/lib/seo'
import ProductGrid from '@/components/themes/shop/ProductGrid'

export const metadata: Metadata = generateSEO({
  title: 'Products - Shop',
  description: 'Browse our collection of premium products',
})

export const revalidate = 3600 // Revalidate every hour

export default async function ProductsPage({
  searchParams,
}: {
  searchParams: { category?: string; search?: string }
}) {
  const products = await productApi.getAll({
    category_id: searchParams.category ? parseInt(searchParams.category) : undefined,
    search: searchParams.search,
  })

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Our Products</h1>
      
      {/* Search and filters */}
      <div className="mb-6 flex gap-4">
        {/* Add search and filter components */}
      </div>

      <ProductGrid products={products.data} />
    </div>
  )
}
```

### 9. Create Product Detail Page (SSG with ISR)

**app/(shop)/products/[slug]/page.tsx:**
```typescript
import { Metadata } from 'next'
import { notFound } from 'next/navigation'
import Image from 'next/image'
import { productApi } from '@/lib/api'
import { generateSEO, generateProductSchema } from '@/lib/seo'
import AddToCartButton from '@/components/themes/shop/AddToCartButton'

export async function generateMetadata({ 
  params 
}: { 
  params: { slug: string } 
}): Promise<Metadata> {
  const product = await productApi.getBySlug(params.slug)
  
  return generateSEO({
    title: product.data.name,
    description: product.data.description,
    ogImage: product.data.images[0]?.url,
  })
}

export const revalidate = 3600 // ISR: Revalidate every hour

export default async function ProductDetailPage({
  params,
}: {
  params: { slug: string }
}) {
  const { data: product } = await productApi.getBySlug(params.slug)

  if (!product) {
    notFound()
  }

  const schema = generateProductSchema(product)

  return (
    <>
      {/* JSON-LD Schema */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
      />

      <div className="container mx-auto px-4 py-8">
        <div className="grid md:grid-cols-2 gap-8">
          {/* Product Images */}
          <div className="space-y-4">
            <div className="aspect-square relative rounded-lg overflow-hidden">
              <Image
                src={product.images[0]?.url || '/placeholder.jpg'}
                alt={product.images[0]?.alt || product.name}
                fill
                className="object-cover"
                priority
                sizes="(max-width: 768px) 100vw, 50vw"
              />
            </div>
            
            {/* Thumbnail gallery */}
            <div className="grid grid-cols-4 gap-2">
              {product.images.slice(1, 5).map((image) => (
                <div key={image.id} className="aspect-square relative rounded-md overflow-hidden">
                  <Image
                    src={image.thumb}
                    alt={image.alt}
                    fill
                    className="object-cover"
                    sizes="(max-width: 768px) 25vw, 12.5vw"
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            <div>
              <h1 className="text-3xl font-bold mb-2">{product.name}</h1>
              {product.category && (
                <p className="text-gray-600">{product.category.name}</p>
              )}
            </div>

            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-bold">{product.price.formatted}</span>
              {product.compare_at_price && (
                <span className="text-xl text-gray-400 line-through">
                  {product.compare_at_price.formatted}
                </span>
              )}
            </div>

            <div className="prose max-w-none">
              <p>{product.description}</p>
            </div>

            {product.in_stock ? (
              <AddToCartButton product={product} />
            ) : (
              <button disabled className="w-full py-3 bg-gray-300 text-gray-600 rounded-lg">
                Out of Stock
              </button>
            )}

            <div className="border-t pt-4 text-sm text-gray-600">
              <p>SKU: {product.sku}</p>
              <p>Stock: {product.stock} units available</p>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
```

### 10. Create Reusable Components

**components/themes/shop/ProductCard.tsx:**
```typescript
import Link from 'next/link'
import Image from 'next/image'
import { Product } from '@/types'

export default function ProductCard({ product }: { product: Product }) {
  return (
    <Link href={`/products/${product.slug}`} className="group">
      <div className="space-y-4">
        <div className="aspect-square relative rounded-lg overflow-hidden bg-gray-100">
          <Image
            src={product.images[0]?.thumb || '/placeholder.jpg'}
            alt={product.images[0]?.alt || product.name}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-300"
            sizes="(max-width: 768px) 50vw, (max-width: 1200px) 33vw, 25vw"
          />
          {!product.in_stock && (
            <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
              <span className="text-white font-semibold">Out of Stock</span>
            </div>
          )}
        </div>

        <div className="space-y-2">
          <h3 className="font-semibold group-hover:text-blue-600 transition-colors">
            {product.name}
          </h3>
          
          <div className="flex items-baseline gap-2">
            <span className="text-lg font-bold">{product.price.formatted}</span>
            {product.compare_at_price && (
              <span className="text-sm text-gray-400 line-through">
                {product.compare_at_price.formatted}
              </span>
            )}
          </div>
        </div>
      </div>
    </Link>
  )
}
```

### 11. Configure Tailwind CSS

**tailwind.config.ts:**
```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          // ... Add full color scale
          900: '#1e3a8a',
        },
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
}
export default config
```

### 12. Optimize Performance

**Image Optimization:**
- Use Next.js Image component
- Specify width/height or fill
- Use appropriate sizes prop
- Enable AVIF/WebP formats

**Font Optimization:**
```typescript
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter'
})
```

**Code Splitting:**
- Use dynamic imports for heavy components
- Implement React.lazy() for client components
- Use route groups for theme separation

## Expected Outputs

### Success
- Next.js application running at http://localhost:3000
- All routes render correctly with SSR/SSG
- Images optimized and lazy-loaded
- SEO meta tags present on all pages
- Core Web Vitals: LCP <2.5s, FID <100ms, CLS <0.1
- Mobile-responsive on all screen sizes

**Lighthouse Scores Target:**
- Performance: 90+
- Accessibility: 95+
- Best Practices: 95+
- SEO: 100

### Failure Scenarios

**1. Image Loading Fails**
- Error: "Invalid src prop"
- Cause: Backend URL not configured in next.config.js
- Solution: Add remote pattern for Laravel storage
- Update directive: Document image domain configuration

**2. Hydration Mismatch**
- Error: "Text content does not match server-rendered HTML"
- Cause: Client/server rendering differences
- Solution: Use `useEffect` for client-only content, `suppressHydrationWarning`
- Update directive: Add hydration debugging steps

**3. API Not Reachable**
- Error: "connect ECONNREFUSED"
- Cause: Docker network issue or wrong API URL
- Solution: Check `NEXT_PUBLIC_API_URL` env var, verify containers are on same network
- Update directive: Add network troubleshooting section

**4. Build Fails**
- Error: "Type error: Cannot find module"
- Cause: Missing TypeScript types or incorrect imports
- Solution: Check import paths, install missing type definitions
- Update directive: Document common type issues

## Edge Cases

### Multi-Language Support
- Use `next-intl` or `next-i18next`
- Create language switcher component
- Store locale in cookies

### Dark Mode
- Use `next-themes` package
- Persist preference in localStorage
- Add toggle in header

### Progressive Web App
- Add `next-pwa` plugin
- Create `manifest.json`
- Implement service worker

## Testing Checklist

After running the script, verify:
- [ ] Next.js dev server running at http://localhost:3000
- [ ] Product listing page loads with data from API
- [ ] Product detail page renders with images
- [ ] Navigation works between pages
- [ ] Images are optimized (check Network tab)
- [ ] Meta tags present in page source
- [ ] JSON-LD schema validates at https://validator.schema.org
- [ ] Mobile responsive (test on Chrome DevTools)
- [ ] Lighthouse audit passes targets
- [ ] Hot reload works for code changes

## Performance Expectations
- Page load: <2 seconds on 3G
- Time to Interactive: <3 seconds
- First Contentful Paint: <1 second
- API calls cached appropriately

## Updates to This Directive

### [2025-02-03] Initial creation
- Created comprehensive Next.js setup directive
- Defined theme system architecture
- Planned SEO optimization strategy

### Future improvements to track:
- ISR revalidation timing optimization
- Image optimization settings that work best
- Bundle size targets
- Caching strategies

---

**Remember:** Next.js is the presentation layer. Keep it thin, delegate business logic to Laravel API. Focus on performance, SEO, and user experience.
