import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // Store the original host to forward to the backend
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set(
    "x-forwarded-host",
    request.headers.get("host") || "localhost:3000",
  );
  requestHeaders.set(
    "x-forwarded-proto",
    request.headers.get("x-forwarded-proto") || "http",
  );
  requestHeaders.set(
    "x-forwarded-port",
    request.headers.get("x-forwarded-port") || "3000",
  );

  return NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  });
}

// Apply to all routes that might be proxied
export const config = {
  matcher: [
    "/admin/:path*",
    "/api/:path*",
    "/sanctum/:path*",
    "/storage/:path*",
    "/livewire/:path*",
  ],
};
