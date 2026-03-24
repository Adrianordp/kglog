from fastapi import FastAPI

from app.core.version import get_version
from app.routers import body_measurements, user

app = FastAPI(
    title="Kg-Log API",
    description="API for Kg-Log application",
    version=get_version(),
    swagger_ui_init_oauth={"usePkceWithAuthorizationCodeGrant": False},
    swagger_ui_parameters={"docExpansion": "none"},
    openapi_tags=[
        {
            "name": "users",
            "description": "Operations related to user management",
        },
        {
            "name": "body_measurements",
            "description": "Operations related to body measurements management",
        },
    ],
)


@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to the Kg-Log API!"}


@app.get("/health", tags=["Health"])
def read_health():
    """Health check endpoint."""
    return {"status": "ok"}


app.include_router(user.router)
app.include_router(body_measurements.router)
