from database import get_db, startup_event
from models import Item
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
app = FastAPI()
app.add_event_handler("startup", startup_event)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"message": "Validation error", "errors": exc.errors()})

@app.post("/items/", status_code=201)
def create_item(item:Item):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, price, is_offer) VALUES (?, ?, ?)", (item.name, item.price, int(item.is_offer) if item.is_offer else None), )
    conn.commit()
    item.id = cursor.lastrowid
    return item

@app.put("/items/{item_id}")
def update_item(item_id:int, item:Item):
    """API route to update an item from database trought the item id.

    Parameters
    ----------
    item_id : int
        Item unique identification
    item : Item
        The item itself following the Item model

    Returns
    -------
    Item
        The item after it has been added to database
    """
    conn = get_db()
    conn.execute(
        "UPDATE items SET name = ?, price = ?, is_offer = ? WHERE id = ?",
        (item.name, item.price, int(item.is_offer) 
        if item.is_offer 
        else None, item_id),)
    conn.commit()
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    API route to delete an item from the database.

    Parameters
    ----------
    item_id : int
        The id of the item to be deleted.

    Returns
    -------
    dict
        A message indicating the deletion was successful.
    """
    conn = get_db()
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    return {"message": "Item deleted"}

@app.get("/items/offers/")
def get_offer_items():
    """
    API route to get all items that are offers.

    Returns
    -------
    List[Item]
        A list of items that are offers.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, is_offer FROM items WHERE is_offer = 1")
    rows = cursor.fetchall()
    return [Item(id=row[0], name=row[1], price=row[2], is_offer=bool(row[3])) for row in rows]

@app.get("/items/count/")
def count_items():
    """
    API route to count the total number of items.

    Returns
    -------
    dict
        A dictionary containing the total count of items.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM items")
    count = cursor.fetchone()[0]
    return {"count": count}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)