from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pizza-ordering-app",
    version="1.0.6",
    author="Alikhan Abdykaimov",
    author_email="2026.alikhan.abdykaimov@uwcisak.jp",
    description="A beautiful pizza ordering application built with KivyMD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/al1kss/pizza-app",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.7",
    install_requires=[
        "kivy>=2.2.0",
        "passlib>=1.7.4",
        "kivymd>=1.2.0",
    ],
    entry_points={
        "console_scripts": [
            "pizza-app=pizza_app.cli:main",
            "pizza-ordering-app=pizza_app.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "pizza_app": [
            "*.kv",
            "assets/images/coke.png",
            "assets/images/fries.png",
            "assets/images/logo.png",
            "assets/images/mushroom.png",
            "assets/images/pizza.png",
            "assets/images/pizza_background.png",
            "assets/databases/login.sql",
            "assets/databases/menu.sql",
            "assets/databases/orders.sql",
        ],
    },
    keywords="kivymd pizza ordering app restaurant gui mobile",
    project_urls={
        "Bug Reports": "https://github.com/al1kss/pizza-app/issues",
        "Source": "https://github.com/al1kss/pizza-app/",
    },
)