from enum import Enum
from typing import Annotated, Literal
from fastapi import Depends, FastAPI, Query, Path
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Model class
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: str | None = None

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

def fake_decode_user(token):
    return User(username=token+"fakedecoded", email="john@examplemail.com", full_name="John Doe" )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_user(token)
    return user

@app.get("/user/me")
async def get_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


# @app.get("/item/")
async def read_item(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token":token}



class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/sum/{num1}/{num2}")
async def sum(num1:int, num2:int):
    return {f"sum of {num1} and {num2}": num1+num2}


# Input according to the model.
# If the input is something else then what is expected which is what's in the Model class, will validate!
@app.get("/model/{model_name}")
async def get_model(model_name:ModelName):

    print(model_name.capitalize())

    if model_name is ModelName.alexnet:
        return {"model_name": ModelName.alexnet, "message":"Deep learning FTW!"}

    if model_name == "lenet":
        return {"model_name":ModelName.lenet, "message":"LeCNN all the images"}

    return {"model_name":ModelName.resnet, "message":"Have some residual"}

# File path

@app.get("/files/{file_path:path}")
async def get_file(file_path: str):
    return {"file path":file_path}

# Required query parameters

# @app.get("/items/{item_id}")
async def read_user_items(item_id:str, req_param:str, skip:int=0, limit:int | None = None):
    item = {"item_id":item_id, "req_param":req_param, "skip":skip, "limit":limit}
    return item


class Item(BaseModel):
    name:        str
    description: str   | None = None
    price:       float
    tax:         float | None = None

# Post request with body

# @app.post("/items/{item_id}")
async def get_body(item_id:int, item:Item, q:str | None = None):
    
    result = {"item_id":item_id, **item.dict()}
    
    if q:
        result.update({"q":q})
    
    return result

# Query parameters and string validations

# @app.get("/items")
async def read_items(
    q: Annotated[
        list[str] | None,
        Query(
            # alias="item-query",
            title="Query String",
            description="Query string for the items to search in the database that have a good match",
            # min_length=3,
            # max_length=50,
            # pattern="^fixedquery$"
        ),
    ] = ['foo','bar','fizz']
):
    query_items = {"q":q}
    return query_items


# Path parameters and numeric validations

# @app.get("/items/{item_id}")
async def validate_numeric_item(
    item_id: Annotated[int, Path(ge=10,le=20)],
    q: str
):
    result = {"item_id":item_id}
    if q:
        result.update({"q":q})
    
    return result



# Query parameters with a pydantic model

class FilterParams(BaseModel):
    model_config = {"extra":"forbid"}
    limit:    int = Field(10, gt=0, le=100)
    offset:   int = Field(0, ge=0)
    order_by: Literal['created_at','updated_at'] = 'created_at'
    tags:     list[str] = []

@app.get("/items/")
async def read_items_from_pydantic_model(filter_query: Annotated[FilterParams, Query()]):
    return filter_query



class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    fullname: str | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id":item_id, "item":item, "user":user}
    return results































# from typing import Annotated

# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pydantic import BaseModel



# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }

# app = FastAPI()

# def fake_hash_password(password: str):
#     return "fakehashed" + password


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


# class UserInDB(User):
#     hashed_password: str


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# def fake_decode_token(token):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_users_db, token)
#     return user


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @app.post("/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     return {"access_token": user.username, "token_type": "bearer"}


# @app.get("/users/me")
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return current_user
