#!/usr/bin/env python3
"""
Setup Next.js Frontend for CMS System
Execution script for directives/generate_nextjs_frontend.md
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import time
import argparse


class NextJsFrontendSetup:
    def __init__(self, theme_style: str = "modern"):
        self.theme_style = theme_style
        self.project_root = Path.cwd()
        self.frontend_dir = self.project_root / "frontend"

    def run_docker_command(
        self, command: list, check: bool = True
    ) -> subprocess.CompletedProcess:
        """Run a command inside the nextjs container"""
        full_command = ["docker", "compose", "exec", "-T", "nextjs"] + command
        print(f"Running: {' '.join(full_command)}")
        try:
            return subprocess.run(
                full_command,
                cwd=self.project_root,
                check=check,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            raise

    def check_nextjs_installed(self) -> bool:
        """Check if package.json exists in frontend and has next"""
        return (self.frontend_dir / "package.json").exists()

    def install_nextjs(self):
        """Install Next.js into the frontend directory"""
        print("\n📦 Installing Next.js...")

        try:
            # 1. Ensure directory is empty-ish (Docker ignores might leave some stuff, but create-next-app needs empty)
            # Since we are mapped to a volume, we might need to be careful.
            # Best approach: create in temp dir inside container, then copy over.

            print("   Creating temp project...")
            # Using --yes to skip prompts
            self.run_docker_command(
                [
                    "npx",
                    "create-next-app@latest",
                    "temp_app",
                    "--typescript",
                    "--tailwind",
                    "--eslint",
                    "--app",
                    "--no-src-dir",
                    "--import-alias",
                    "@/*",
                    "--use-npm",
                    "--no-git",
                    "--yes",
                ]
            )

            # 2. Move files from temp_app to root
            print("   Moving files to root...")
            move_cmd = ["sh", "-c", "cp -rT temp_app . && rm -rf temp_app"]
            self.run_docker_command(move_cmd)

            print("✓ Next.js initialized successfully")

        except Exception as e:
            print(f"✗ Failed to install Next.js: {e}")
            sys.exit(1)

    def install_dependencies(self):
        """Install additional dependencies"""
        print("\n📚 Installing additional packages...")
        packages = [
            "@tanstack/react-query",
            "axios",
            "zod",
            "react-hook-form",
            "clsx",
            "tailwind-merge",
        ]

        dev_packages = ["@tailwindcss/typography", "@tailwindcss/forms"]

        try:
            self.run_docker_command(["npm", "install"] + packages)
            self.run_docker_command(["npm", "install", "-D"] + dev_packages)
            print("✓ Dependencies installed")
        except Exception as e:
            print(f"✗ Failed to install dependencies: {e}")

    def create_directory_structure(self):
        """Create the folder structure specified in the directive"""
        print("\nStructure creating...")

        dirs = [
            "app/(shop)/products/[slug]",
            "app/(shop)/cart",
            "app/(shop)/checkout",
            "app/(travel)/tours/[slug]",
            "app/(travel)/booking",
            "app/(restaurant)/menu",
            "app/(restaurant)/reservation",
            "app/(corporate)/services",
            "app/(corporate)/portfolio",
            "app/(corporate)/about",
            "app/(corporate)/contact",
            "app/api/revalidate",
            "components/shared",
            "components/themes/shop",
            "components/themes/travel",
            "components/themes/restaurant",
            "components/themes/corporate",
            "lib",
            "types",
            "public/images",
            "public/fonts",
            "public/icons",
        ]

        # We can create these locally since the volume is mounted
        # BUT 'src' dir option might have been used or not.
        # The directive said "--no-src-dir" but my install command used "--src-dir" by default in recent versions if not specified?
        # Actually I passed "--src-dir" in install_nextjs.
        # So everything is inside src/ ?
        # Wait, the directive said `create-next-app ... --no-src-dir`.
        # My install command used `--src-dir`. I should correct that to match directive if possible,
        # OR just adapt. Let's stick to directive: `--no-src-dir` implies code is in root `app/`.
        # However, I passed `--src-dir` in the code above (line 55).
        # I will FIX install_nextjs to use `--no-src-dir` to match the directive exactly.

        for d in dirs:
            dir_path = self.frontend_dir / d
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   Created {d}")

    def create_api_client(self):
        """Create lib/api.ts"""
        content = """import axios from 'axios'

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

export default api
"""
        with open(self.frontend_dir / "lib/api.ts", "w") as f:
            f.write(content)
        print("✓ Created lib/api.ts")

    def run(self):
        print("🚀 Setting up Next.js Frontend...")

        # Check if already installed
        if self.check_nextjs_installed():
            print("ℹ️ Next.js already initialized. Skipping install.")
        else:
            self.install_nextjs()

        self.install_dependencies()

        # We need to make sure we are not using 'src' directory if we want to follow structure
        # My install command in 'install_nextjs' used --src-dir.
        # I will update the install command in the actual execution to --no-src-dir
        # But since I am writing the file now, I will fix it in the class method above before writing.

        self.create_directory_structure()
        self.create_api_client()

        print("\n✨ Frontend setup complete!")
        print("   URL: http://localhost:3000")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme", default="modern")
    args = parser.parse_args()

    setup = NextJsFrontendSetup(theme_style=args.theme)
    setup.run()


if __name__ == "__main__":
    main()
