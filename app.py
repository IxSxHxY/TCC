from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import get_engine, ItemOperation
from pydantic import BaseModel
from typing import Annotated, Union, Optional
from starlette.middleware.sessions import SessionMiddleware
import typing

def flash(request: Request, message: typing.Any, category: str = "") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append({"message": message, "category": category})


def get_flashed_messages(request: Request):
    print(request.session)
    return request.session.pop("_messages") if "_messages" in request.session else []

username="root"
password=""
hostname="localhost"
port="3306"
database_name="TCC"

database = get_engine(
    username=username,
    password=password,
    hostname=hostname,
    port=port,
    database_name=database_name,
    use_memory=False)
item_ops = ItemOperation(database)



app = FastAPI()
templates = Jinja2Templates(directory="templates")


origins = ["*"]
app.add_middleware(
 CORSMiddleware,
 allow_origins=origins,
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
)
app.add_middleware(
 SessionMiddleware,
 secret_key='super-secret'
)

templates.env.globals['get_flashed_messages'] = get_flashed_messages

@app.get("/test")
async def test():
 return "Hello World!"

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request, query: str=""):
    items = item_ops.query_item_using_string(query=query)
    return templates.TemplateResponse("home_page.html", {"request": request, "items": items, 'query': query})


@app.get("/add_item", response_class=HTMLResponse)
async def add_item_page(request: Request):
    return templates.TemplateResponse("add_item.html", {"request": request, "username": "Ivan"})

@app.post("/add_item", response_class=RedirectResponse)
async def add_item(request: Request, item_name: str = Form(), item_price: float =Form(), item_count: int = Form(), item_description: Optional[str] = Form(None)):
    if not item_ops.check_exists_with_name(item_name):
        flash(request=request, message="Exists the item with the same name", category="error")
    else: 
        item_ops.add_item(name=item_name, description=item_description, price=item_price, count=item_count)
        flash(request=request, message="Item added successfully!", category="success")
    
    return RedirectResponse("./add_item", status_code=303)
#     # return templates.TemplateResponse("add_item.html", {"request": request, "username": "Ivan"})

@app.get("/delete_item/{item_id}", response_class=RedirectResponse)
async def delete_item(item_id: int, request: Request):
    if item_ops.check_exists_with_id(item_id):
        item_ops.delete_item(id=item_id)
        flash(request=request, message=f"Item with id = {item_id} deleted successfully", category="success")
    else:
        flash(request=request, message=f"Item with id = {item_id} does not exists", category="error")
    return RedirectResponse("/", status_code=303)

@app.post("/edit_item/{item_id}", response_class=RedirectResponse)
async def edit_item(request: Request, item_id: int, item_name: str = Form(), item_price: float =Form(), item_count: int = Form(), item_description: Optional[str] = Form(None)):
    if not item_ops.check_exists_with_id(item_id):
        flash(request=request, message=f"Item with id = {item_id} does not exists", category="error")
        return RedirectResponse("/", status_code=303)
    updated_data = {
        'name': item_name,
        'description': item_description,
        'price': item_price,
        'count': item_count
    }
    item = item_ops.edit_item(id=item_id, updated_data=updated_data)
    flash(request=request, message=f"Item had been updated successfully!", category="success")
    return RedirectResponse(f"/edit_item/{item_id}", status_code=303)

@app.get("/edit_item/{item_id}", response_class=[HTMLResponse, RedirectResponse])
async def edit_item_page(request: Request, item_id: int):
    if not item_ops.check_exists_with_id(item_id):
        flash(request=request, message=f"Item with id = {item_id} does not exists", category="error")
        return RedirectResponse("/", status_code=303)
    item = item_ops.query_item_using_id(id=item_id)
    return templates.TemplateResponse("edit_item.html", {"request": request, "item": item})

@app.get("/remove_item/{item_name}", response_class=HTMLResponse)
async def read_root(item_name: str, request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request, "username": "Ivan"})
