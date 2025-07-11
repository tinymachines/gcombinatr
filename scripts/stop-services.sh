#!/bin/bash
# Stop all GCombinatr services

echo "🛑 Stopping GCombinatr services..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Stop Redis
echo -n "Stopping Redis... "
if command_exists redis-cli; then
    redis-cli shutdown >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Stopped${NC}"
    else
        echo -e "${YELLOW}Not running${NC}"
    fi
else
    echo -e "${RED}Not installed${NC}"
fi

# Stop Neo4j
echo -n "Stopping Neo4j... "
if command_exists neo4j; then
    neo4j stop >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Stopped${NC}"
    else
        echo -e "${YELLOW}Not running or needs sudo${NC}"
    fi
else
    echo -e "${RED}Not installed${NC}"
fi

# Stop MongoDB
echo -n "Stopping MongoDB... "
if command_exists mongod; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew services stop mongodb-community >/dev/null 2>&1
    else
        # Linux
        sudo systemctl stop mongod >/dev/null 2>&1
    fi
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Stopped${NC}"
    else
        echo -e "${YELLOW}Not running${NC}"
    fi
else
    echo -e "${RED}Not installed${NC}"
fi

# Stop InfluxDB
echo -n "Stopping InfluxDB... "
if command_exists influxd; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew services stop influxdb >/dev/null 2>&1
    else
        # Linux
        sudo systemctl stop influxdb >/dev/null 2>&1
    fi
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Stopped${NC}"
    else
        echo -e "${YELLOW}Not running${NC}"
    fi
else
    echo -e "${RED}Not installed${NC}"
fi

# Stop Kafka (optional)
echo -n "Stopping Kafka (optional)... "
# Find Kafka installation
KAFKA_HOME=""
if [ -d "/usr/local/kafka" ]; then
    KAFKA_HOME="/usr/local/kafka"
elif [ -d "$HOME/kafka" ]; then
    KAFKA_HOME="$HOME/kafka"
fi

if [ -n "$KAFKA_HOME" ]; then
    # Stop Kafka
    $KAFKA_HOME/bin/kafka-server-stop.sh >/dev/null 2>&1
    sleep 2
    # Stop Zookeeper
    $KAFKA_HOME/bin/zookeeper-server-stop.sh >/dev/null 2>&1
    echo -e "${GREEN}Stopped${NC}"
else
    echo -e "${YELLOW}Not installed (optional)${NC}"
fi

# Stop Ollama (optional)
echo -n "Stopping Ollama (optional)... "
if command_exists ollama; then
    pkill -f "ollama serve" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Stopped${NC}"
    else
        echo -e "${YELLOW}Not running${NC}"
    fi
else
    echo -e "${YELLOW}Not installed (optional)${NC}"
fi

echo ""
echo "✅ All services stopped!"
echo ""
echo "To start services again, run:"
echo "  ./scripts/start-services.sh"