from fastapi import FastAPI, status, HTTPException


app = FastAPI()


@app.get("/", status_code=200)
def read_root():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/add/{a}/{b}", status_code=200)
def add(a: str, b: str):
    """
    Add two numbers together.
    
    Parameters:
    - a: First number
    - b: Second number
    
    Returns:
    - JSON object with the result
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Both 'a' and 'b' must be valid numbers")
    return {"result": a + b}


@app.get("/subtract/{a}/{b}", status_code=200)
def subtract(a: str, b: str):
    """
    Subtract two numbers.
    
    Parameters:
    - a: First number
    - b: Second number
    
    Returns:
    - JSON object with the result
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Both 'a' and 'b' must be valid numbers")
    return {"result": a - b}
   

@app.get("/multiply/{a}/{b}", status_code=200)
def multiply(a: str, b: str):
    """
    Multiply two numbers together.
    
    Parameters:
    - a: First number
    - b: Second number
    
    Returns:
    - JSON object with the result
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Both 'a' and 'b' must be valid numbers")
    return {"result": a * b}   


@app.get("/divide/{a}/{b}", status_code=200)
def divide(a: str, b: str):
    """
    Divide two numbers.
    
    Parameters:
    - a: First number
    - b: Second number
    
    Returns:
    - JSON object with the result
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Both 'a' and 'b' must be valid numbers")
    return {"result": a / b}


@app.get("/average/{a}/{b}/{c}/{d}", status_code=200)
def average(a: str, b: str):
    """
    Calculates the average of four numbers.
    
    Parameters:
    - a: First number
    - b: Second number
    - c: Third number
    - d: Fourth number
    
    Returns:
    - JSON object with the result
    """
    try:
        a = float(a)
        b = float(b)
        c = float(c)
        d = float(d)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="All parameters 'a', 'b', 'c', and 'd' must be valid numbers")
    return {"result": (a + b + c + d) / 4}
    

@app.get("/tip/{bill_amount}/{tip_percent}", status_code=200)
def tip_calculator(bill_amount: str, tip_percent: str):
    """
    Find the remainder of 'a' divided by 'b'.
    
    Parameters:
    - bill_amount: Bill amount
    - tip_percent: Tip percent
    
    Returns:
    - JSON object with the result
    """
    try:
        bill_amount = float(bill_amount)
        tip_percent = float(tip_percent)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Both 'bill_amount' and 'tip_percent' must be valid numbers")
    if bill_amount < 0 or tip_percent < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="'bill_amount' and 'tip_percent' cannot be negative")
    tip_amount = bill_amount * (tip_percent / 100)
    total_bill = bill_amount + tip_amount
    return {"Tip Amount": tip_amount, "Total Bill Amount": total_bill}


@app.get("/percentage/{part}/{whole}", status_code=200)
def percentage(part: str, whole: str):
    """
    Calculate what percent the 'part' is of the 'whole.'
    
    Parameters:
    - part: Part value
    - whole: Whole value
    
    Returns:
    - JSON object with the result
    """
    try:
        part = float(part)
        whole = float(whole)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Both 'part' and 'whole' must be valid numbers")
    if whole == 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="The 'whole' cannot be zero")
    return {"result": ((part / whole) * 100)}