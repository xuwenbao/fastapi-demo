from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_demo.models.diocese import Diocese
from fastapi_demo.services import get_session
from fastapi_demo.api import router


def create_app():
    """Create the FastAPI app and include the router."""
    app = FastAPI(
        title="My application",
        description="A FastAPI app for demonstrating SQLModel",
        version="0.0.1",
    )

    origins = [
        '*',
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.include_router(router=router)

    @app.get('/health')
    def get_health():
        return {'status': 'OK'}
    
    return app

app = create_app()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=7860, workers=1)