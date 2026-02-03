---
name: frontend-dev
description: comprehensive guide for building Next.js 14+ frontends with premium design and SEO. Use when creating pages, components, layouts, or optimizing site performance.
license: Complete terms in LICENSE.txt
---

# Frontend Development (Next.js + Design + SEO)

This skill guides the creation of high-performance, aesthetically premium Next.js applications.

## 🎨 Design Philosophy (Clean Luxury / Refined)

When building UI, always adhere to the **Refined/Luxury** aesthetic unless specified otherwise.
- **Typography**: Use distinct pairings (e.g., Playfair Display + Inter/Sans). Avoid generic system fonts for headings.
- **Spacing**: generous negative space ("air") to create elegance.
- **Motion**: Subtle entrance animations (`animate-in`, `fade-in`), micro-interactions on hover.
- **Visuals**: Use high-quality imagery, subtle gradients/mesh, or noise textures. Avoid flat, solid primary colors.
- **Dark Mode**: Prioritize deep, rich dark modes (`bg-zinc-950` or `#0a0a0a`) over pure black.

## ⚡ Framework Standards (Next.js 14+)

### 1. App Router
- Use the **App Router** (`app/`) directory structure.
- **Server Components**: Default to Server Components. Only use `'use client'` for interactive islands (forms, listeners).
- **Layouts**: Use `layout.tsx` for shared shells (navbars, footers).

### 2. Styling (Tailwind CSS)
- **Utility First**: Use Tailwind utility classes.
- **Arbitrary Values**: Use `[]` for precise design tokens (e.g., `h-[500px]`, `bg-[#0a0a0a]`) if config tokens aren't sufficient for the *premium* feel.
- **CN Helper**: Use `clsx` or `tailwind-merge` for conditional classes.

### 3. Images
- Always use `next/image`.
- Define `width`/`height` or `fill`.
- Configure `remotePatterns` in `next.config.ts` for external hosts (Unsplash, etc.).

## 🔍 SEO Strategy

Every page MUST include metadata.

### 1. Metadata API
Use the Next.js Metadata API in `page.tsx` or `layout.tsx`:

```tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Page Title | Brand Name',
  description: 'Compelling description for search engines.',
  openGraph: {
    title: 'Page Title',
    description: 'Compelling description.',
    url: 'https://site.com/page',
    siteName: 'Brand Name',
    images: [
      {
        url: 'https://site.com/og.jpg',
        width: 1200,
        height: 630,
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
}
```

### 2. Semantic HTML
- Use proper heading hierarchy (`h1` -> `h2` -> `h3`).
- Use `<main>`, `<section>`, `<article>`, `<header>`, `<footer>`.
- Always add `alt` text to images.

## 🚀 Workflow

1. **Structure**: Create directory `app/[route]/`.
2. **Page**: Create `page.tsx`.
3. **Meta**: Export `metadata` object.
4. **Layout**: (Optional) Create `layout.tsx` if unique UI shell is needed.
5. **Components**: Build UI, extracted to `components/` if reusable.
6. **Polishing**: Add animations and verify mobile responsiveness.
