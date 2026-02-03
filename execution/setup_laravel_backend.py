#!/usr/bin/env python3
"""
Setup Laravel Backend for CMS System
Execution script for directives/setup_laravel_backend.md
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import time
import argparse


class LaravelBackendSetup:
    def __init__(self, admin_panel: str = "filament"):
        self.admin_panel = admin_panel
        self.project_root = Path.cwd()
        self.backend_dir = self.project_root / "backend"

    def run_docker_command(
        self, command: list, check: bool = True
    ) -> subprocess.CompletedProcess:
        """Run a command inside the laravel container"""
        full_command = ["docker", "compose", "exec", "-T", "laravel"] + command
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

    def check_laravel_installed(self) -> bool:
        """Check if composer.json exists in backend"""
        return (self.backend_dir / "composer.json").exists()

    def install_laravel(self):
        """Install Laravel into the backend directory"""
        print("\n📦 Installing Laravel...")

        # We need to install into a temp directory because backend/ is not empty
        # (contains Dockerfile, .env, etc.)
        try:
            # 1. Create project in temp folder inside container
            print("   Creating temp project...")
            self.run_docker_command(
                [
                    "composer",
                    "create-project",
                    "laravel/laravel:^11.0",
                    "temp_app",
                    "--prefer-dist",
                    "--no-interaction",
                ]
            )

            # 2. Move files from temp_app to root
            print("   Moving files to root...")
            # We use a shell script inside docker to move files
            move_cmd = ["sh", "-c", "cp -rT temp_app . && rm -rf temp_app"]
            self.run_docker_command(move_cmd)

            # 3. Fix permissions
            print("   Fixing permissions...")
            self.run_docker_command(
                [
                    "chown",
                    "-R",
                    "www-data:www-data",
                    "storage",
                    "bootstrap/cache",
                ]
            )
            self.run_docker_command(
                ["chmod", "-R", "775", "storage", "bootstrap/cache"]
            )

            print("✓ Laravel installed successfully")

        except Exception as e:
            print(f"✗ Failed to install Laravel: {e}")
            sys.exit(1)

    def install_dependencies(self):
        """Install required packages"""
        print("\n📚 Installing dependencies...")
        packages = [
            "laravel/sanctum",
            "spatie/laravel-permission",
            "spatie/laravel-medialibrary",
            "spatie/laravel-sluggable",
        ]

        for package in packages:
            try:
                print(f"   Installing {package}...")
                self.run_docker_command(["composer", "require", package])
            except Exception as e:
                print(f"✗ Failed to install {package}: {e}")
                # Don't exit, might be non-critical or recoverable

    def install_admin_panel(self):
        """Install Admin Panel"""
        print(f"\n🔐 Installing Admin Panel ({self.admin_panel})...")

        try:
            if self.admin_panel == "filament":
                print("   Requiring filament/filament...")
                self.run_docker_command(
                    [
                        "composer",
                        "require",
                        "filament/filament:^3.2",
                        "--no-interaction",
                    ]
                )

                print("   Installing Filament...")
                self.run_docker_command(
                    [
                        "php",
                        "artisan",
                        "filament:install",
                        "--panels",
                        "--no-interaction",
                    ]
                )

            elif self.admin_panel == "nova":
                print(
                    "⚠ Nova installation requires a license key and auth.json. Skipping exact steps."
                )
                print(
                    "   Please install Nova manually or provide credentials."
                )

        except Exception as e:
            print(f"✗ Failed to install admin panel: {e}")

    def run_migrations(self):
        """Run database migrations"""
        print("\n🗄️ Running migrations...")
        try:
            # Wait for DB to be ready
            print("   Waiting for database...")
            time.sleep(5)

            self.run_docker_command(["php", "artisan", "migrate", "--force"])
            print("✓ Migrations completed")
        except Exception as e:
            print(f"✗ Failed to run migrations: {e}")

    def run(self):
        """Main execution flow"""
        print("🔧 Setting up Laravel Backend...")

        if self.check_laravel_installed():
            print(
                "ℹ️ Laravel already installed (composer.json found). Skipping installation."
            )
        else:
            self.install_laravel()

        self.install_dependencies()
        self.install_admin_panel()
        self.run_migrations()

        print("\n" + "=" * 50)
        print("🎉 Laravel Backend Setup Complete!")
        print("=" * 50)
        print(f"\n📍 URLs:")
        print(f"   API:        http://localhost:8000")
        print(f"   Admin:      http://localhost:8000/admin")
        print("\n📝 Default Admin Login:")
        print(
            "   (You may need to create a user: docker compose exec laravel php artisan make:filament-user)"
        )


def main():
    parser = argparse.ArgumentParser(description="Setup Laravel Backend")
    parser.add_argument(
        "--admin-panel",
        default="filament",
        choices=["filament", "nova"],
        help="Admin panel to install",
    )
    args = parser.parse_args()

    setup = LaravelBackendSetup(admin_panel=args.admin_panel)
    setup.run()


if __name__ == "__main__":
    main()
