"""
Simple startup script for the Research Paper Generator API.
Run this to start the FastAPI server.
"""
import uvicorn

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🚀 Starting Research Paper Generator API Server")
    print("="*80)
    print("\n📡 Server will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("📚 Alternative Docs: http://localhost:8000/redoc")
    print("\n💡 Tip: Use Ctrl+C to stop the server")
    print("="*80 + "\n")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
