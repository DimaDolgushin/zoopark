import fastapi
import uvicorn
import settings
from fastapi.responses import RedirectResponse
from src.server.router import routers


app = fastapi.FastAPI(title="ZooApp", version="0.1 Alpha")

[app.include_router(router) for router in routers]


@app.router.get(path='/', include_in_schema=False)
def index():
    return RedirectResponse(url='/docs')


if __name__ == "__main__":
    uvicorn.run(app=settings.APP, reload=True, host=settings.HOST, port=settings.PORT)
