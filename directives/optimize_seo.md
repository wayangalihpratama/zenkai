# Directive: SEO Optimization & Google Indexing

## Goal
Ensure all CMS websites are fully optimized for search engines, achieve maximum visibility in Google Search, and maintain excellent Core Web Vitals scores.

## Prerequisites
- Next.js frontend deployed and accessible
- Laravel backend serving content via API
- Google Search Console access
- Cloudflare account (optional but recommended)

## Inputs
- `website_type` (enum): "shop" | "travel" | "restaurant" | "corporate"
- `target_keywords` (array): Primary keywords for SEO
- `locale` (string): "id" (Indonesian) or "en" (English)

## Execution Tool
**Script:** `execution/optimize_seo.py`

## SEO Checklist

### 1. Technical SEO

#### Server-Side Rendering (SSR)
- ✅ All pages use Next.js App Router with SSR or SSG
- ✅ Dynamic pages use `generateStaticParams` for static generation
- ✅ Implement ISR (Incremental Static Regeneration) for frequently changing content

#### Meta Tags
Every page must have:
```typescript
export const metadata: Metadata = {
  title: 'Page Title - 60 chars max',
  description: 'Meta description 150-160 chars',
  robots: 'index,follow',
  alternates: {
    canonical: 'https://yourdomain.com/page-url',
  },
  openGraph: {
    title: 'Page Title',
    description: 'Description',
    url: 'https://yourdomain.com/page-url',
    images: [{ url: 'https://yourdomain.com/og-image.jpg' }],
  },
}
```

#### Structured Data (JSON-LD)
Implement appropriate schemas for each website type:

**Shop - Product Schema:**
```json
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "Product Name",
  "image": ["url1", "url2"],
  "description": "Product description",
  "sku": "SKU123",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product",
    "priceCurrency": "IDR",
    "price": "150000",
    "availability": "https://schema.org/InStock"
  }
}
```

**Travel - Tour Schema:**
```json
{
  "@context": "https://schema.org/",
  "@type": "TouristTrip",
  "name": "Tour Name",
  "description": "Tour description",
  "itinerary": {
    "@type": "ItemList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Day 1: Destination"
      }
    ]
  }
}
```

**Restaurant - Restaurant Schema:**
```json
{
  "@context": "https://schema.org/",
  "@type": "Restaurant",
  "name": "Restaurant Name",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "Jakarta",
    "addressCountry": "ID"
  },
  "servesCuisine": "Indonesian",
  "priceRange": "$$",
  "telephone": "+62-21-1234567"
}
```

**Corporate - Organization Schema:**
```json
{
  "@context": "https://schema.org/",
  "@type": "Organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://facebook.com/company",
    "https://twitter.com/company"
  ]
}
```

### 2. Performance Optimization

#### Core Web Vitals Targets
- **LCP (Largest Contentful Paint)**: <2.5 seconds
- **FID (First Input Delay)**: <100 milliseconds
- **CLS (Cumulative Layout Shift)**: <0.1

#### Image Optimization
```typescript
import Image from 'next/image'

<Image
  src="/product.jpg"
  alt="Descriptive alt text with keywords"
  width={800}
  height={600}
  priority // For above-the-fold images
  sizes="(max-width: 768px) 100vw, 50vw"
  quality={85}
/>
```

#### Font Optimization
```typescript
import { Inter } from 'next/font/google'

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
  preload: true
})
```

#### Code Splitting
```typescript
// Dynamic imports for heavy components
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />,
  ssr: false // Client-side only if needed
})
```

### 3. Content Optimization

#### URL Structure
✅ Good:
- `/products/premium-coffee-beans`
- `/tours/bali-adventure-package`
- `/menu/signature-nasi-goreng`

❌ Bad:
- `/products/123`
- `/p?id=456`

#### Headings Hierarchy
```html
<h1>Page Title (One per page)</h1>
<h2>Main Sections</h2>
<h3>Subsections</h3>
```

#### Alt Text for Images
```typescript
<Image 
  src={product.image}
  alt={`${product.name} - ${product.category} - Buy online`}
/>
```

#### Internal Linking
- Link related products
- Connect blog posts
- Create breadcrumb navigation

### 4. XML Sitemap

Generate dynamic sitemap at `/sitemap.xml`:

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const products = await getProducts()
  
  const productUrls = products.map((product) => ({
    url: `https://yourdomain.com/products/${product.slug}`,
    lastModified: product.updated_at,
    changeFrequency: 'daily' as const,
    priority: 0.8,
  }))

  return [
    {
      url: 'https://yourdomain.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    ...productUrls,
  ]
}
```

### 5. Robots.txt

```typescript
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin/', '/api/', '/checkout/'],
      },
    ],
    sitemap: 'https://yourdomain.com/sitemap.xml',
  }
}
```

### 6. Mobile Optimization

#### Responsive Design
- Use Tailwind breakpoints: `sm:`, `md:`, `lg:`, `xl:`
- Test on multiple devices
- Ensure touch targets are 44x44px minimum

#### Mobile Speed
- Reduce initial bundle size
- Lazy load images below the fold
- Use modern image formats (WebP, AVIF)

### 7. Indonesian SEO Specifics

#### Language Tags
```typescript
export const metadata: Metadata = {
  alternates: {
    languages: {
      'id-ID': 'https://yourdomain.com/id',
      'en-US': 'https://yourdomain.com/en',
    },
  },
}
```

#### Local Business Schema (for Restaurant/Shop with physical location)
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Jalan Sudirman No. 123",
    "addressLocality": "Jakarta Selatan",
    "addressRegion": "DKI Jakarta",
    "postalCode": "12190",
    "addressCountry": "ID"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": -6.2088,
    "longitude": 106.8456
  },
  "telephone": "+62-21-1234567"
}
```

#### Indonesian Keywords
- Research using Google Keyword Planner (Indonesia)
- Include local terms: "Jual", "Beli", "Harga", "Murah"
- Use Indonesian address format

### 8. Google Search Console Setup

#### Submit Sitemap
1. Verify domain ownership
2. Submit sitemap URL: `https://yourdomain.com/sitemap.xml`
3. Monitor indexing status

#### Request Indexing
```bash
# Use Google Search Console API or manual submission
# For new pages, request immediate indexing
```

### 9. Page Speed Insights

Target scores:
- Mobile: 90+
- Desktop: 95+

Optimization tips:
- Enable compression (Brotli/Gzip)
- Use CDN (Cloudflare)
- Minimize JavaScript
- Defer non-critical CSS

### 10. Schema Validation

Tools:
- https://validator.schema.org/
- Google Rich Results Test
- Ensure no errors in structured data

## Testing Checklist

- [ ] All pages have unique titles and descriptions
- [ ] Structured data validates without errors
- [ ] Images have descriptive alt text
- [ ] URLs are clean and include keywords
- [ ] Core Web Vitals pass on mobile and desktop
- [ ] Sitemap generates correctly
- [ ] Robots.txt allows search engines
- [ ] Mobile responsive on all screen sizes
- [ ] Page load time <3 seconds
- [ ] HTTPS enabled
- [ ] Canonical URLs set correctly
- [ ] No duplicate content
- [ ] Internal linking structure logical
- [ ] 404 pages customized
- [ ] Redirects (301) for changed URLs

## Performance Expectations

- Initial indexing: 24-48 hours after submission
- Full site crawl: 1-2 weeks
- Ranking improvements: 2-3 months with consistent optimization

## Monitoring

### Weekly Checks
- Google Search Console for errors
- Core Web Vitals scores
- Indexing status

### Monthly Checks
- Keyword rankings
- Organic traffic growth
- Page speed insights
- Competitor analysis

## Edge Cases

### Dynamic Content
- Use ISR with appropriate revalidation time
- Cache at CDN level for static assets

### User-Generated Content
- Noindex pages with thin content
- Implement pagination for large lists

### Multi-Language Sites
- Use `hreflang` tags
- Separate sitemaps per language

## Updates to This Directive

### [2025-02-03] Initial creation
- Created comprehensive SEO optimization directive
- Defined technical SEO requirements
- Planned schema implementations per website type

### Future improvements to track:
- Actual Core Web Vitals scores achieved
- Indexing speed improvements
- Successful schema implementations
- Any SEO issues encountered

---

**Remember:** SEO is ongoing. Continuously monitor, test, and improve. Content quality matters as much as technical optimization.
