#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path


def setup_app_directory():
    home_dir = Path.home()
    app_dir = home_dir / ".pizza_app"

    app_dir.mkdir(exist_ok=True)

    package_dir = Path(__file__).parent

    user_assets_dir = app_dir / "assets"
    if not user_assets_dir.exists():
        package_assets_dir = package_dir / "assets"
        if package_assets_dir.exists():
            shutil.copytree(package_assets_dir, user_assets_dir)

    kv_file = app_dir / "pizza.kv"
    if not kv_file.exists():
        package_kv = package_dir / "pizza.kv"
        if package_kv.exists():
            shutil.copy2(package_kv, kv_file)

    return app_dir


def main():
    try:
        # Setup app directory and files
        app_dir = setup_app_directory()

        original_dir = os.getcwd()
        os.chdir(app_dir)

        package_dir = Path(__file__).parent
        sys.path.insert(0, str(package_dir))

        from pizza_app.main import MainApp

        print("🍕 Starting Pizza Ordering App...")
        print(f"📁 App data stored in: {app_dir}")
        print("📱 Close the app window to exit")

        app = MainApp()
        app.run()

    except ImportError as e:
        print(f"❌ Error importing required modules: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install kivymd kivy passlib")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        sys.exit(1)
    finally:
        try:
            os.chdir(original_dir)
        except:
            pass


if __name__ == "__main__":
    main()