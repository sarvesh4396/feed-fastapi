from app.core import auth_backend, current_active_user, fastapi_users
from app.core import settings
from app.core import UserCreate, UserRead, UserUpdate
from app.core import notifier
from app.db import User, create_db_and_tables
from fastapi import Depends, FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi import WebSocket,WebSocketDisconnect
from .feed import html
from fastapi.routing import APIRouter


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
callback_router = APIRouter()


@app.get("/")
def about():
    return {"message": "How you doing?"}


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"],
    callbacks = callback_router.routes
    
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
    callbacks = callback_router.routes
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

@callback_router.get("/push")
async def push_message(user:User = Depends(current_active_user)):
    message = f"User {user.email} Logged in"
    await notifier.push(message)

app.include_router(callback_router)

@app.get("/feed",tags=["feed"])
async def feed():
    return HTMLResponse(html)





@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        notifier.remove(websocket)

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    await notifier.generator.asend(None)






