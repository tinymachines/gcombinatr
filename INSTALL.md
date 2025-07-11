# Installation Guide - Docker-less Setup

This guide provides instructions for setting up GCombinatr without Docker, installing all required services directly on your system.

## Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows (with WSL2)
- **Python**: 3.11 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 20GB free space
- **GPU**: Optional but recommended for ML features

### Required Services
The following services need to be installed and running:
- Redis
- Neo4j
- MongoDB
- InfluxDB
- Kafka (optional for event streaming)
- Ollama (optional for AI features)

## Step-by-Step Installation

### 1. Install Python 3.11+

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

#### macOS (using Homebrew)
```bash
brew install python@3.11
```

#### Windows
Download and install from [python.org](https://www.python.org/downloads/)

### 2. Install Required Services

#### Redis

**Ubuntu/Debian:**
```bash
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**macOS:**
```bash
brew install redis
brew services start redis
```

**Windows (WSL2):**
Follow Ubuntu instructions above

#### Neo4j

**All platforms:**
1. Download Neo4j Community Edition from [neo4j.com](https://neo4j.com/download/)
2. Extract and run:
```bash
# Linux/macOS
./bin/neo4j start

# Or install via package manager
# Ubuntu/Debian
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j
sudo systemctl start neo4j

# macOS
brew install neo4j
brew services start neo4j
```

Default credentials: neo4j/neo4j (you'll be prompted to change on first login)

#### MongoDB

**Ubuntu/Debian:**
```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Create list file
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Install MongoDB
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### InfluxDB

**All platforms:**
```bash
# Download and install InfluxDB 2.x
# Ubuntu/Debian
wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.7.1-amd64.deb
sudo dpkg -i influxdb2-2.7.1-amd64.deb
sudo systemctl start influxdb
sudo systemctl enable influxdb

# macOS
brew install influxdb
brew services start influxdb
```

Setup InfluxDB:
1. Navigate to http://localhost:8086
2. Create initial user and organization
3. Save the generated token for .env configuration

#### Kafka (Optional)

**Ubuntu/Debian:**
```bash
# Install Java (required for Kafka)
sudo apt install default-jdk

# Download Kafka
wget https://downloads.apache.org/kafka/3.6.0/kafka_2.13-3.6.0.tgz
tar -xzf kafka_2.13-3.6.0.tgz
cd kafka_2.13-3.6.0

# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties &

# Start Kafka
bin/kafka-server-start.sh config/server.properties &
```

**macOS:**
```bash
brew install kafka
brew services start zookeeper
brew services start kafka
```

#### Ollama (Optional, for AI features)

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
# Pull the codellama model
ollama pull codellama
```

**macOS:**
```bash
# Download from https://ollama.ai/download
# Or use brew
brew install ollama
ollama serve &
ollama pull codellama
```

### 3. Clone and Setup GCombinatr

```bash
# Clone the repository
git clone https://github.com/yourusername/gcombinatr.git
cd gcombinatr

# Create virtual environment
python3.11 -m venv ecosystem-lab
source ecosystem-lab/bin/activate  # On Windows: ecosystem-lab\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# For development
pip install -e ".[dev]"
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

Update the following in `.env`:
- Add your GitHub tokens (comma-separated)
- Set Neo4j password (if changed from default)
- Add InfluxDB token and organization
- Adjust other settings as needed

### 5. Verify Installation

Run the verification script:
```bash
# Create a verification script
python -c "
import sys
print(f'Python version: {sys.version}')

try:
    import redis
    r = redis.Redis()
    r.ping()
    print('✓ Redis connection successful')
except Exception as e:
    print(f'✗ Redis connection failed: {e}')

try:
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver('neo4j://localhost:7687', auth=('neo4j', 'password'))
    driver.verify_connectivity()
    print('✓ Neo4j connection successful')
    driver.close()
except Exception as e:
    print(f'✗ Neo4j connection failed: {e}')

try:
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    client.admin.command('ping')
    print('✓ MongoDB connection successful')
except Exception as e:
    print(f'✗ MongoDB connection failed: {e}')

try:
    from influxdb_client import InfluxDBClient
    client = InfluxDBClient(url='http://localhost:8086', token='your-token')
    client.ping()
    print('✓ InfluxDB connection successful')
except Exception as e:
    print(f'✗ InfluxDB connection failed: {e}')
"
```

### 6. Initialize the Ecosystem

```bash
# Run initial setup
python -m gcombinatr.setup.initialize

# Seed with initial organisms (when implemented)
python -m gcombinatr.seeder --source github --query "python" --limit 10

# Start the ecosystem (when implemented)
python -m gcombinatr.ecosystem.run --population 100 --generations 10
```

## Service Management

### Starting Services

Create a startup script `start-services.sh`:
```bash
#!/bin/bash
echo "Starting GCombinatr services..."

# Start Redis
redis-server --daemonize yes

# Start Neo4j
neo4j start

# Start MongoDB
sudo systemctl start mongod

# Start InfluxDB
sudo systemctl start influxdb

# Start Kafka (if using)
# cd /path/to/kafka
# bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
# bin/kafka-server-start.sh -daemon config/server.properties

# Start Ollama (if using)
# ollama serve &

echo "All services started!"
```

### Stopping Services

Create a shutdown script `stop-services.sh`:
```bash
#!/bin/bash
echo "Stopping GCombinatr services..."

# Stop Redis
redis-cli shutdown

# Stop Neo4j
neo4j stop

# Stop MongoDB
sudo systemctl stop mongod

# Stop InfluxDB
sudo systemctl stop influxdb

# Stop Kafka (if using)
# cd /path/to/kafka
# bin/kafka-server-stop.sh
# bin/zookeeper-server-stop.sh

echo "All services stopped!"
```

Make scripts executable:
```bash
chmod +x start-services.sh stop-services.sh
```

## Troubleshooting

### Port Conflicts
If services fail to start due to port conflicts:
- Redis: Default port 6379
- Neo4j: Default ports 7474 (HTTP), 7687 (Bolt)
- MongoDB: Default port 27017
- InfluxDB: Default port 8086
- Kafka: Default port 9092

Check what's using a port:
```bash
sudo lsof -i :PORT_NUMBER
```

### Permission Issues
Some services may require sudo. Consider:
- Adding your user to required groups
- Adjusting service configurations
- Using user-space installations where possible

### Memory Issues
If services consume too much memory:
1. Adjust service configurations
2. Limit cache sizes
3. Run fewer services concurrently

## Development Setup

For development work:
```bash
# Install development dependencies
pip install -e ".[dev,ml,monitoring]"

# Set up pre-commit hooks (when configured)
pre-commit install

# Run tests
pytest tests/

# Run linting
black src/
pylint src/
mypy src/
```

## Next Steps

1. Configure your GitHub tokens in `.env`
2. Adjust ecosystem parameters in configuration
3. Start developing or run the example ecosystem
4. Monitor services at:
   - Neo4j Browser: http://localhost:7474
   - InfluxDB: http://localhost:8086
   - MongoDB: Use a GUI like MongoDB Compass

## Alternative: Using Python-only Dependencies

For a minimal setup without external services, you can use:
- SQLite instead of Neo4j/MongoDB
- In-memory caching instead of Redis
- File-based metrics instead of InfluxDB

This requires code modifications but eliminates service dependencies.