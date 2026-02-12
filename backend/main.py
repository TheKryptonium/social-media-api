from fastapi import FastAPI


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('src.app:app', reload=True, port=5001)
