# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GCombinatr is a Python project that transforms GitHub gists into autonomous digital organisms that evolve, communicate, and self-organize. The project is inspired by bacterial behavior and powered by genetic programming to create a living ecosystem where code evolves.

## Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv ecosystem-lab
source ecosystem-lab/bin/activate  # Linux/Mac
# or
ecosystem-lab\Scripts\activate  # Windows

# Install dependencies (when requirements.txt is created)
pip install -r requirements.txt
```

### Running the Application
```bash
# Start infrastructure services
docker-compose up -d

# Seed organisms from GitHub
python -m gcombinatr.seeder --source github --query "python data processing" --limit 100

# Run ecosystem simulation
python -m gcombinatr.ecosystem.run --population 500 --generations 1000
```

### Development Tools
```bash
# Code formatting
black src/

# Linting
pylint src/

# Type checking
mypy src/

# Run tests
pytest tests/ -v
```

## Architecture Overview

### Core Components

1. **Organism System** (`src/organisms/`)
   - `GitHubOrganism`: Base class for digital bacteria created from gists
   - AST-based genome representation for code mutation
   - Membrane, metabolism, and signal systems for biological behaviors

2. **Evolution Engine** (`src/evolution/`)
   - Genetic programming with AST-level mutations
   - Multi-objective fitness evaluation
   - Speciation and adaptive mutation rates

3. **Ecosystem** (`src/ecosystem/`)
   - 2D spatial environment with resource gradients
   - Population dynamics and carrying capacity
   - Catastrophe recovery mechanisms

4. **GitHub Integration** (`src/core/`)
   - Rate-limited GitHub API client with token rotation
   - ETAG caching for efficient API usage
   - Gist discovery and transformation pipeline

### Data Storage
- **Neo4j**: Organism relationships and evolutionary lineage
- **MongoDB**: Gist content and metadata storage
- **Redis**: Caching and real-time ecosystem state
- **InfluxDB**: Time-series metrics for evolution tracking

### Key Technologies
- **Python 3.11+** with async/await patterns
- **Docker** for containerized services
- **Kafka** for event-driven architecture
- **Grafana** for ecosystem monitoring (http://localhost:3000)

## Implementation Status

The project is in early development with extensive documentation but no implementation yet. Key tasks from THE-PLAN.md include:

1. Setting up project structure and configuration system
2. Implementing GitHub API client with rate limiting
3. Creating database layers for polyglot persistence
4. Building the organism transformation pipeline
5. Developing the evolution engine
6. Creating ecosystem simulation environment

## Important Notes

- The project uses biological metaphors throughout (organisms, evolution, ecosystems)
- All code execution happens in sandboxed containers for safety
- Multiple GitHub tokens are recommended for rate limit management
- The system is designed for high scalability with distributed components
- Focus on emergent behaviors rather than predetermined outcomes