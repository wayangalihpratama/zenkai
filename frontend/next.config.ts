import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "images.unsplash.com",
      },
    ],
  },
  async rewrites() {
    return [
      {
        source: "/admin",
        destination: "http://laravel:80/admin",
      },
      {
        source: "/admin/:path*",
        destination: "http://laravel:80/admin/:path*",
      },
      {
        source: "/api/:path*",
        destination: "http://laravel:80/api/:path*",
      },
      {
        source: "/sanctum/:path*",
        destination: "http://laravel:80/sanctum/:path*",
      },
      {
        source: "/storage/:path*",
        destination: "http://laravel:80/storage/:path*",
      },
      {
        source: "/livewire/:path*",
        destination: "http://laravel:80/livewire/:path*",
      },
      {
        source: "/css/:path*",
        destination: "http://laravel:80/css/:path*",
      },
      {
        source: "/js/:path*",
        destination: "http://laravel:80/js/:path*",
      },
    ];
  },
};

export default nextConfig;
