#!/bin/bash

# Aviation Weather MCP Server Startup Script
# This script ensures the server starts correctly with proper environment setup

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}Aviation Weather MCP Server Startup Script${NC}"
echo "============================================"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.8+ is available
check_python() {
    print_status "Checking Python version..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        print_status "Found Python $PYTHON_VERSION"
        
        # Check if version is 3.8 or higher
        if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
            print_status "Python version is compatible"
        else
            print_error "Python 3.8+ is required. Found: $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 is not installed or not in PATH"
        exit 1
    fi
}

# Check if pip is available
check_pip() {
    print_status "Checking pip availability..."
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is not installed or not in PATH"
        exit 1
    fi
    print_status "pip3 is available"
}

# Install dependencies if needed
install_dependencies() {
    print_status "Checking dependencies..."
    
    # Check if package is installed in development mode
    if pip3 show aviation-weather-mcp &> /dev/null; then
        print_status "Package is already installed"
    else
        print_status "Installing package in development mode..."
        pip3 install -e .
    fi
    
    # Verify key dependencies
    python3 -c "import mcp, httpx, fastapi" 2>/dev/null || {
        print_error "Required dependencies are missing. Installing..."
        pip3 install -e .
    }
    
    print_status "Dependencies are ready"
}

# Function to check if port is in use
check_port() {
    local port=$1
    if command -v netstat &> /dev/null; then
        if netstat -tln | grep -q ":$port "; then
            return 0  # Port is in use
        fi
    elif command -v lsof &> /dev/null; then
        if lsof -i :$port &> /dev/null; then
            return 0  # Port is in use
        fi
    fi
    return 1  # Port is free
}

# Kill existing processes
cleanup_existing() {
    print_status "Checking for existing server processes..."
    
    # Find and kill existing processes
    PIDS=$(pgrep -f "aviation_weather_mcp" 2>/dev/null || true)
    if [ -n "$PIDS" ]; then
        print_warning "Found existing server processes: $PIDS"
        echo "$PIDS" | xargs kill -TERM 2>/dev/null || true
        sleep 2
        # Force kill if still running
        PIDS=$(pgrep -f "aviation_weather_mcp" 2>/dev/null || true)
        if [ -n "$PIDS" ]; then
            echo "$PIDS" | xargs kill -KILL 2>/dev/null || true
        fi
        print_status "Cleaned up existing processes"
    fi
}

# Parse command line arguments
MODE="sse"
PORT="8003"
HOST="localhost"

while [[ $# -gt 0 ]]; do
    case $1 in
        --mode|-m)
            MODE="$2"
            shift 2
            ;;
        --port|-p)
            PORT="$2"
            shift 2
            ;;
        --host|-h)
            HOST="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --mode, -m    Server mode: 'sse' or 'stdio' (default: sse)"
            echo "  --port, -p    Port for SSE mode (default: 8003)"
            echo "  --host, -h    Host for SSE mode (default: localhost)"
            echo "  --help        Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate mode
if [[ "$MODE" != "sse" && "$MODE" != "stdio" ]]; then
    print_error "Invalid mode: $MODE. Must be 'sse' or 'stdio'"
    exit 1
fi

# Main startup sequence
main() {
    print_status "Starting Aviation Weather MCP Server..."
    print_status "Mode: $MODE"
    
    if [[ "$MODE" == "sse" ]]; then
        print_status "Host: $HOST"
        print_status "Port: $PORT"
        
        # Check if port is in use
        if check_port "$PORT"; then
            print_warning "Port $PORT is already in use"
            print_status "Attempting to clean up existing processes..."
            cleanup_existing
            sleep 1
            if check_port "$PORT"; then
                print_error "Port $PORT is still in use after cleanup"
                exit 1
            fi
        fi
    fi
    
    # Setup checks
    check_python
    check_pip
    install_dependencies
    cleanup_existing
    
    print_status "Environment setup complete"
    echo ""
    
    # Create log directory if it doesn't exist
    mkdir -p logs
    
    # Set environment variables
    export PYTHONPATH="$SCRIPT_DIR/src:$PYTHONPATH"
    
    # Start the server based on mode
    if [[ "$MODE" == "sse" ]]; then
        print_status "Starting server in SSE mode on $HOST:$PORT..."
        echo -e "${BLUE}Server will be available at: http://$HOST:$PORT/sse${NC}"
        echo "Press Ctrl+C to stop the server"
        echo ""
        
        # Set FastMCP environment variables to ensure consistency
        export FASTMCP_HOST="$HOST"
        export FASTMCP_PORT="$PORT"
        
        # Start server with proper environment
        python3 -m aviation_weather_mcp sse 2>&1 | tee "logs/server-$(date +%Y%m%d-%H%M%S).log"
        
    elif [[ "$MODE" == "stdio" ]]; then
        print_status "Starting server in STDIO mode..."
        print_warning "STDIO mode is for MCP client connections only"
        echo "Press Ctrl+C to stop the server"
        echo ""
        
        # Start server in stdio mode
        python3 -m aviation_weather_mcp --stdio 2>&1 | tee "logs/server-$(date +%Y%m%d-%H%M%S).log"
    fi
}

# Trap Ctrl+C to cleanup
cleanup_on_exit() {
    print_status "Shutting down server..."
    cleanup_existing
    exit 0
}

trap cleanup_on_exit INT TERM

# Run main function
main "$@"
