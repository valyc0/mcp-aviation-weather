import asyncio
import typer
import os

from .server import run_sse, run_stdio

app = typer.Typer(help="Aviation Weather MCP Server")

@app.command()
def sse(
    port: int = typer.Option(None, "--port", "-p", help="Port to listen on (default: 8000 or FASTMCP_PORT env var)"),
    host: str = typer.Option(None, "--host", "-h", help="Host to bind to (default: 127.0.0.1 or FASTMCP_HOST env var)")
):
    """Start Aviation Weather MCP Server in SSE mode"""
    # Set environment variables if provided via command line
    if port is not None:
        os.environ["FASTMCP_PORT"] = str(port)
    if host is not None:
        os.environ["FASTMCP_HOST"] = host
    
    # Get final values for display
    final_port = os.environ.get("FASTMCP_PORT", "8000")
    final_host = os.environ.get("FASTMCP_HOST", "127.0.0.1")
    
    print("Aviation Weather MCP Server - SSE mode")
    print("--------------------------------------")
    print(f"Server will start on {final_host}:{final_port}")
    print("Press Ctrl+C to exit")
    try:
        asyncio.run(run_sse())
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Service stopped.")

@app.command()
def stdio():
    """Start Aviation Weather MCP Server in stdio mode"""
    try:
        run_stdio()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Service stopped.")

if __name__ == "__main__":
    app()
