from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from .core.config import get_settings
from .core.logging import configure_logging
from .core.security import require_api_key
from .graphql.schema import schema


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(level=settings.log_level)

    app = FastAPI(title="Cargo (GraphQL)")

    # CORS
    if settings.allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    async def context_getter(_=Depends(require_api_key)):
        # Put shared resources into context if needed
        return {}

    gql = GraphQLRouter(schema, context_getter=context_getter)
    app.include_router(gql, prefix="/graphql")

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.get("/ready")
    async def ready():
        return {"status": "ready"}

    return app
