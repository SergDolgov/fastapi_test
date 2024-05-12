from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from database import create_tables, delete_tables
# from router import router as users_router
from auth.auth_router import auth_router
from user.user_router import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    await delete_tables()

    await create_tables()

    yield
    print("Application closed.")

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(user_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello():
    return "Hello"