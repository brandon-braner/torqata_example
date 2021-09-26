from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from app.config import settings
from app.cors import get_cors_domains
from app.modules.user.authentication_controller import router as authentication_router

app = FastAPI()


def main():
    configure(settings.app_env)


def configure(env: str):
    configure_cors(env)
    configure_middleware()
    configure_routes()


def configure_cors(env: str):
    origins = get_cors_domains(env)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def configure_middleware():
    from app.middleware.authentication_middleware import AuthBackend
    app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())


def configure_db():
    pass


def configure_routes():
    @app.get("/health")
    async def root():
        return {"message": "Health Response"}

    # Routes from other routers
    app.include_router(authentication_router)


if __name__ == "__main__":
    main()
else:
    configure(settings.app_env)
