import uvicorn

from settings import settings

if __name__ == "__main__":
    uvicorn.run(
        app="app.app:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.IS_DEBUG,
    )
