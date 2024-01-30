from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

app = FastAPI(
    title="Trading App"
)

#send server error info to the user
@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )




fake_users = [
    {"id": 1, "role": "admin", "name": ["Bob"], "degree": [
        {"id": 1, "created_at": "2024-01-01T00:00:00", "type_degree": "expert"}]},
    {"id": 2, "role": "trader", "name": "Allan", "degree": [
        {"id": 2, "created_at": "2024-01-01T00:00:00", "type_degree": "middle"}]},
    {"id": 3, "role": "investor", "name": "James"}
]

fake_users2 = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "trader", "name": "Allan"},
    {"id": 3, "role": "investor", "name": "James"}
]

fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC",
        "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC",
        "side": "sell", "price": 125, "amount": 2.12},

]

# uvicorn main:app --reload


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


class DegreeType(Enum):
    junior = "junior"
    middle = "middle"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


@app.get("/trades")
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]


@app.post("/users/{user_id}")
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id")
                        == user_id, fake_users2))[0]
    current_user["name"] = new_name
    return {"status": 200, "data": current_user}
