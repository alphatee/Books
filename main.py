from datetime import datetime
from decimal import Decimal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field # what is field ?

app = FastAPI()

class Book(BaseModel):
    isbn: str = None
    title: str = ""
    author: str = ""
    pages: int = 0
    price: Decimal = Decimal(0)
    # Use Field(default_factory=datetime.now) for a dynamic timestamp
    publication_date: datetime = Field(default_factory=datetime.now)
    famous_quote: str = ""

# key is isbn, the value is the book
books = {} # create a dictionary

@app.get("/")
async def root():
    return {"message": "Hello, Welcome to my Book Store."}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

############################
# Create CRUD for Book API #
############################
@app.post("/books", response_model=Book)
async def create_book(book: Book) -> Book:
    if book.isbn in books:
        raise HTTPException(status_code=400, detail=f"isbn: {book.isbn} already exists")
    else:
        books[book.isbn] = book
        return book

@app.get("/books", response_model=dict[str, Book])
async def get_all_books() -> dict[str, Book]:
    if not books: # checks if dictionary is empty
        raise HTTPException(status_code=400, detail="The store is empty")
    else:
        return books

@app.get("/book/{isbn}", response_model=Book)
async def get_book(isbn: str) -> Book:
    if isbn in books:
        return books[isbn]
    else:
        raise HTTPException(status_code=404, detail=f"The isbn: {isbn} was not found")
