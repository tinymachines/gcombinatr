#!/usr/bin/env python3
"""
Service Verification Script for GCombinatr
Checks if all required services are running and accessible
"""

import sys
import os
from typing import Tuple, List
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def check_python_version() -> Tuple[bool, str]:
    """Check if Python version is 3.11 or higher"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        return True, f"{version.major}.{version.minor}.{version.micro}"
    return False, f"{version.major}.{version.minor}.{version.micro} (3.11+ required)"

def check_redis() -> Tuple[bool, str]:
    """Check Redis connectivity"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        info = r.info()
        return True, f"v{info.get('redis_version', 'unknown')}"
    except ImportError:
        return False, "redis package not installed"
    except Exception as e:
        return False, str(e)

def check_neo4j() -> Tuple[bool, str]:
    """Check Neo4j connectivity"""
    try:
        from neo4j import GraphDatabase
        # Try default credentials
        driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))
        driver.verify_connectivity()
        driver.close()
        return True, "Connected (neo4j://localhost:7687)"
    except ImportError:
        return False, "neo4j package not installed"
    except Exception as e:
        if "authentication" in str(e).lower():
            return False, "Authentication failed (check credentials)"
        return False, str(e)

def check_mongodb() -> Tuple[bool, str]:
    """Check MongoDB connectivity"""
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        # Force connection
        client.admin.command('ping')
        server_info = client.server_info()
        version = server_info.get('version', 'unknown')
        client.close()
        return True, f"v{version}"
    except ImportError:
        return False, "pymongo package not installed"
    except Exception as e:
        return False, str(e)

def check_influxdb() -> Tuple[bool, str]:
    """Check InfluxDB connectivity"""
    try:
        from influxdb_client import InfluxDBClient
        # Check if token is set in environment
        token = os.getenv('INFLUXDB_TOKEN', 'your-token')
        client = InfluxDBClient(url="http://localhost:8086", token=token, timeout=2000)
        if client.ping():
            return True, "Connected (http://localhost:8086)"
        return False, "Ping failed"
    except ImportError:
        return False, "influxdb-client package not installed"
    except Exception as e:
        if "401" in str(e):
            return False, "Authentication failed (check token)"
        return False, str(e)

def check_kafka() -> Tuple[bool, str]:
    """Check Kafka connectivity"""
    try:
        from aiokafka import AIOKafkaProducer
        import asyncio
        
        async def test_kafka():
            producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
            try:
                await asyncio.wait_for(producer.start(), timeout=2.0)
                await producer.stop()
                return True, "Connected (localhost:9092)"
            except asyncio.TimeoutError:
                return False, "Connection timeout"
            except Exception as e:
                return False, str(e)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(test_kafka())
        loop.close()
        return result
    except ImportError:
        return False, "aiokafka package not installed"
    except Exception as e:
        return False, str(e)

def check_ollama() -> Tuple[bool, str]:
    """Check Ollama connectivity"""
    try:
        import httpx
        response = httpx.get("http://localhost:11434/api/tags", timeout=2.0)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                model_names = [m.get('name', '') for m in models]
                return True, f"Models: {', '.join(model_names[:3])}"
            return True, "Connected (no models pulled)"
        return False, f"HTTP {response.status_code}"
    except ImportError:
        return False, "httpx package not installed"
    except Exception as e:
        return False, str(e)

def main():
    """Run all service checks"""
    console.print("\n[bold cyan]GCombinatr Service Verification[/bold cyan]\n")
    
    # Define services to check
    services = [
        ("Python Version", check_python_version, True),
        ("Redis", check_redis, True),
        ("Neo4j", check_neo4j, True),
        ("MongoDB", check_mongodb, True),
        ("InfluxDB", check_influxdb, True),
        ("Kafka", check_kafka, False),  # Optional
        ("Ollama", check_ollama, False),  # Optional
    ]
    
    # Create results table
    table = Table(title="Service Status", show_header=True, header_style="bold magenta")
    table.add_column("Service", style="cyan", width=20)
    table.add_column("Status", justify="center", width=12)
    table.add_column("Details", style="dim", width=50)
    table.add_column("Required", justify="center", width=10)
    
    all_required_ok = True
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        
        for service_name, check_func, is_required in services:
            task = progress.add_task(f"Checking {service_name}...", total=None)
            
            try:
                is_ok, details = check_func()
            except Exception as e:
                is_ok, details = False, f"Error: {str(e)}"
            
            progress.remove_task(task)
            
            status_icon = "✅" if is_ok else "❌"
            status_color = "green" if is_ok else "red"
            required_text = "Yes" if is_required else "No"
            required_color = "yellow" if is_required else "dim"
            
            if is_required and not is_ok:
                all_required_ok = False
            
            table.add_row(
                service_name,
                f"[{status_color}]{status_icon}[/{status_color}]",
                details,
                f"[{required_color}]{required_text}[/{required_color}]"
            )
    
    console.print(table)
    
    # Print summary
    console.print("\n[bold]Summary:[/bold]")
    if all_required_ok:
        console.print("✅ All required services are running!", style="bold green")
        console.print("\nYou're ready to start the GCombinatr ecosystem! 🚀")
    else:
        console.print("❌ Some required services are not running.", style="bold red")
        console.print("\nPlease check the [bold]INSTALL.md[/bold] file for setup instructions.")
        console.print("Run [bold cyan]./scripts/start-services.sh[/bold cyan] to start all services.")
    
    # Check environment file
    if os.path.exists('.env'):
        console.print("\n✅ .env file found", style="green")
    else:
        console.print("\n⚠️  .env file not found. Run: [bold]cp .env.example .env[/bold]", style="yellow")
    
    return 0 if all_required_ok else 1

if __name__ == "__main__":
    sys.exit(main())