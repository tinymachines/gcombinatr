from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gcombinatr",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Digital evolution ecosystem where GitHub gists become living organisms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gcombinatr",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Life",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=[
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "PyGithub>=2.1.1",
        "aiohttp>=3.9.1",
        "neo4j>=5.15.0",
        "motor>=3.3.2",
        "redis>=5.0.1",
        "aiokafka>=0.10.0",
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "numpy>=1.26.2",
        "scikit-learn>=1.3.2",
        "astor>=0.8.1",
        "click>=8.1.7",
        "rich>=13.7.0",
        "loguru>=0.7.2",
    ],
    extras_require={
        "dev": [
            "black>=23.12.0",
            "pylint>=3.0.3",
            "mypy>=1.7.1",
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
        ],
        "ml": [
            "ollama>=0.1.7",
            "transformers>=4.36.0",
            "torch>=2.1.2",
        ],
        "monitoring": [
            "prometheus-client>=0.19.0",
            "grafana-api>=1.0.3",
            "plotly>=5.18.0",
            "dash>=2.14.1",
            "influxdb-client>=1.38.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gcombinatr=gcombinatr.cli:main",
        ],
    },
)