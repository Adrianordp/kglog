from fastapi import FastAPI

from app.core.version import get_version

app = FastAPI(
    title="Kg-Log API",
    description="API for Kg-Log application",
    version=get_version(),
    swagger_ui_init_oauth={"usePkceWithAuthorizationCodeGrant": False},
    swagger_ui_parameters={"docExpansion": "none"},
)

@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to the Kg-Log API!"}

@app.get("/health", tags=["Health"])
def read_health():
    """Health check endpoint."""
    return {"status": "ok"}