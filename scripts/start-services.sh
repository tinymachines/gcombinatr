#!/bin/bash
# Start all GCombinatr services

echo "🚀 Starting GCombinatr services..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a service is running
is_running() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Start Redis
echo -n "Starting Redis... "
if command_exists redis-server; then
    if is_running 6379; then
        echo -e "${YELLOW}Already running${NC}"
    else
        redis-server --daemonize yes >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Started${NC}"
        else
            echo -e "${RED}Failed${NC}"
        fi
    fi
else
    echo -e "${RED}Not installed${NC}"
fi

# Start Neo4j
echo -n "Starting Neo4j... "
if command_exists neo4j; then
    if is_running 7687; then
        echo -e "${YELLOW}Already running${NC}"
    else
        neo4j start >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Started${NC}"
        else
            echo -e "${RED}Failed (may need sudo)${NC}"
        fi
    fi
else
    echo -e "${RED}Not installed${NC}"
fi

# Start MongoDB
echo -n "Starting MongoDB... "
if command_exists mongod; then
    if is_running 27017; then
        echo -e "${YELLOW}Already running${NC}"
    else
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            brew services start mongodb-community >/dev/null 2>&1
        else
            # Linux
            sudo systemctl start mongod >/dev/null 2>&1
        fi
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Started${NC}"
        else
            echo -e "${RED}Failed${NC}"
        fi
    fi
else
    echo -e "${RED}Not installed${NC}"
fi

# Start InfluxDB
echo -n "Starting InfluxDB... "
if command_exists influxd; then
    if is_running 8086; then
        echo -e "${YELLOW}Already running${NC}"
    else
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            brew services start influxdb >/dev/null 2>&1
        else
            # Linux
            sudo systemctl start influxdb >/dev/null 2>&1
        fi
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Started${NC}"
        else
            echo -e "${RED}Failed${NC}"
        fi
    fi
else
    echo -e "${RED}Not installed${NC}"
fi

# Start Kafka (optional)
echo -n "Starting Kafka (optional)... "
if [ -d "/usr/local/kafka" ] || [ -d "$HOME/kafka" ]; then
    if is_running 9092; then
        echo -e "${YELLOW}Already running${NC}"
    else
        # Find Kafka installation
        KAFKA_HOME=""
        if [ -d "/usr/local/kafka" ]; then
            KAFKA_HOME="/usr/local/kafka"
        elif [ -d "$HOME/kafka" ]; then
            KAFKA_HOME="$HOME/kafka"
        fi
        
        if [ -n "$KAFKA_HOME" ]; then
            # Start Zookeeper first
            $KAFKA_HOME/bin/zookeeper-server-start.sh -daemon $KAFKA_HOME/config/zookeeper.properties
            sleep 2
            # Start Kafka
            $KAFKA_HOME/bin/kafka-server-start.sh -daemon $KAFKA_HOME/config/server.properties
            echo -e "${GREEN}Started${NC}"
        else
            echo -e "${YELLOW}Skipped${NC}"
        fi
    fi
else
    echo -e "${YELLOW}Not installed (optional)${NC}"
fi

# Start Ollama (optional)
echo -n "Starting Ollama (optional)... "
if command_exists ollama; then
    if is_running 11434; then
        echo -e "${YELLOW}Already running${NC}"
    else
        ollama serve >/dev/null 2>&1 &
        echo -e "${GREEN}Started${NC}"
    fi
else
    echo -e "${YELLOW}Not installed (optional)${NC}"
fi

echo ""
echo "✅ Service startup complete!"
echo ""
echo "To verify all services are running correctly, run:"
echo "  python scripts/verify-services.py"
echo ""
echo "Service URLs:"
echo "  - Redis:    redis://localhost:6379"
echo "  - Neo4j:    http://localhost:7474 (Browser)"
echo "  - MongoDB:  mongodb://localhost:27017"
echo "  - InfluxDB: http://localhost:8086"
echo "  - Kafka:    localhost:9092 (if installed)"
echo "  - Ollama:   http://localhost:11434 (if installed)"