import { Playfair_Display, Inter } from "next/font/google";
import Image from "next/image";
import Link from "next/link";

const playfair = Playfair_Display({ subsets: ["latin"], weight: ["400", "600", "700"] });
const inter = Inter({ subsets: ["latin"], weight: ["300", "400", "500"] });

export default function LoginPage() {
  return (
    <div className={`flex min-h-screen w-full bg-[#0a0a0a] text-zinc-100 selection:bg-amber-900/40 selection:text-amber-100 ${inter.className}`}>

      {/* Mobile Header / Brand (Visible only on mobile/tablet) */}
      <div className="absolute top-0 left-0 z-20 w-full p-6 lg:hidden">
        <span className={`text-xl font-bold tracking-widest text-white ${playfair.className}`}>ZENKAI</span>
      </div>

      {/* Left Column: Visual/Brand */}
      <div className="relative hidden w-full lg:block lg:w-[45%] xl:w-[40%]">
        {/* Background Image with Overlay */}
        <div className="absolute inset-0 z-0">
          <Image
            src="https://images.unsplash.com/photo-1493606371202-6275828f90f3?q=80&w=2561&auto=format&fit=crop"
            alt="Minimalist Architecture"
            fill
            className="object-cover opacity-60 grayscale filter transition-all duration-1000 animate-in fade-in zoom-in-105"
            priority
          />
          <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/20 to-[#0a0a0a]" />
          <div className="absolute inset-0 bg-[url('/noise.png')] opacity-[0.03] mix-blend-overlay" /> {/* Texture if available, otherwise subtle fallback */}
        </div>

        {/* Brand Content */}
        <div className="relative z-10 flex h-full flex-col justify-between p-12 xl:p-16">
          <span className={`text-2xl font-bold tracking-[0.2em] text-white ${playfair.className}`}>
            ZENKAI
          </span>

          <div className="space-y-6">
            <h2 className={`text-4xl font-light leading-tight text-white/90 xl:text-5xl ${playfair.className} animate-in slide-in-from-bottom-4 duration-700`}>
              The art of <br />
              <span className="italic text-amber-100/90">digital presence.</span>
            </h2>
            <div className="h-px w-12 bg-amber-500/50" />
            <p className="max-w-md text-sm font-light leading-relaxed text-zinc-400 animate-in slide-in-from-bottom-5 duration-1000 delay-150">
              Experience a content management system designed for speed, beauty, and absolute control.
            </p>
          </div>

          <div className="flex items-center gap-4 text-xs tracking-wider text-zinc-500 uppercase">
             <span>Est. 2026</span>
             <span className="h-0.5 w-0.5 rounded-full bg-zinc-600" />
             <span>Jakarta, ID</span>
          </div>
        </div>
      </div>

      {/* Right Column: Authentication Form */}
      <div className="flex w-full flex-col justify-center px-6 py-20 lg:w-[55%] lg:px-20 xl:w-[60%] xl:px-32">
        <div className="mx-auto w-full max-w-[420px] animate-in slide-in-from-bottom-8 duration-700 fade-in fill-mode-backwards">

          {/* Header */}
          <div className="mb-10 text-center lg:text-left">
            <h1 className={`text-3xl font-medium text-white ${playfair.className}`}>
              Welcome back
            </h1>
            <p className="mt-3 text-sm text-zinc-400 font-light">
              Enter your credentials to access your dashboard.
            </p>
          </div>

          {/* Form */}
          <form className="space-y-6">
            <div className="space-y-5">
              <div className="group relative">
                <input
                  type="email"
                  id="email"
                  placeholder=" "
                  required
                  className="peer block w-full appearance-none border-b border-zinc-800 bg-transparent px-0 py-3 text-base text-white placeholder-transparent focus:border-amber-100/50 focus:outline-none focus:ring-0 transition-colors"
                />
                <label
                  htmlFor="email"
                  className="absolute left-0 top-3 -translate-y-7 text-xs tracking-wide text-zinc-500 transition-all duration-200 peer-placeholder-shown:translate-y-0 peer-placeholder-shown:text-base peer-placeholder-shown:text-zinc-500 peer-focus:-translate-y-7 peer-focus:text-xs peer-focus:text-amber-100/70 cursor-text"
                >
                  Email Address
                </label>
              </div>

              <div className="group relative">
                <input
                  type="password"
                  id="password"
                  placeholder=" "
                  required
                  className="peer block w-full appearance-none border-b border-zinc-800 bg-transparent px-0 py-3 text-base text-white placeholder-transparent focus:border-amber-100/50 focus:outline-none focus:ring-0 transition-colors"
                />
                <label
                  htmlFor="password"
                  className="absolute left-0 top-3 -translate-y-7 text-xs tracking-wide text-zinc-500 transition-all duration-200 peer-placeholder-shown:translate-y-0 peer-placeholder-shown:text-base peer-placeholder-shown:text-zinc-500 peer-focus:-translate-y-7 peer-focus:text-xs peer-focus:text-amber-100/70 cursor-text"
                >
                  Password
                </label>
              </div>
            </div>

            <div className="flex items-center justify-between pt-2">
              <div className="flex items-center gap-2">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 rounded border-zinc-800 bg-zinc-900/50 text-amber-600 focus:ring-amber-900/20 focus:ring-offset-0 focus:ring-offset-transparent cursor-pointer"
                />
                <label htmlFor="remember-me" className="text-xs text-zinc-400 cursor-pointer select-none hover:text-zinc-300">
                  Remember me
                </label>
              </div>

              <Link
                href="#"
                className="text-xs font-medium text-amber-100/60 hover:text-amber-100 hover:underline hover:underline-offset-4 transition-all"
              >
                Forgot password?
              </Link>
            </div>

            <button
              type="submit"
              className="group relative flex w-full justify-center overflow-hidden rounded-sm bg-white px-4 py-3.5 text-sm font-semibold tracking-wide text-black transition-all hover:bg-zinc-200 focus:outline-none focus:ring-2 focus:ring-zinc-400 focus:ring-offset-2 focus:ring-offset-black mt-8"
            >
              <span className="relative z-10 text-[0.8rem] uppercase tracking-[0.15em]">Sign In</span>
            </button>
          </form>

          {/* Footer */}
          <div className="mt-10 text-center lg:text-left">
            <p className="text-xs text-zinc-500">
              Not a member?{" "}
              <Link href="#" className="font-medium text-white hover:text-amber-100/80 transition-colors">
                Request Access
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
