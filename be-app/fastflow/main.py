# -------------------------
# src/fastflow/main.py
# -------------------------
from fastapi import FastAPI
from .core.config import settings
from .api.v1.router import api_router


def create_app() -> FastAPI:
app = FastAPI(title=settings.APP_NAME)
app.include_router(api_router, prefix='/api')


@app.get('/health')
async def health():
return {'status': 'ok'}


return app


app = create_app()