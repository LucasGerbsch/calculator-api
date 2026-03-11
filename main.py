from fastapi import FastAPI, status, HTTPException, Depends
from google.cloud import bigquery


app = FastAPI()

# Dependency method to provide a BigQuery client
# This will be used by the other endpoints where a database connection is necessary
def get_bq_client():
    # client automatically uses Cloud Run's service account credentials
    client = bigquery.Client()
    try:
        yield client
    finally:
        client.close()

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
    - JSON object with the result of the addition operation. 
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Both 'a' and 'b' must be valid numbers.")
    return {"operation": "addition", "a": a, "b": b,"result": a + b}


@app.get("/subtract/{a}/{b}", status_code=200)
def subtract(a: str, b: str):
    """
    Subtract two numbers.
    
    Parameters:
    - a: First number
    - b: Second number
    
    Returns:
    - JSON object with the result of the subtraction operation.
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Both 'a' and 'b' must be valid numbers")
    return {"operation": "subtraction", "a": a, "b": b,"result": a - b}
   

@app.get("/multiply/{a}/{b}", status_code=200)
def multiply(a: str, b: str):
    """
    Multiply two numbers together.
    
    Parameters:
    - a: First number
    - b: Second number
    
    Returns:
    - JSON object with the result of the multiplication operation.
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Both 'a' and 'b' must be valid numbers")
    return {"operation": "multiplication", "a": a, "b": b,"result": a * b}   


@app.get("/divide/{a}/{b}", status_code=200)
def divide(a: str, b: str):
    """
    Divide two numbers.
    
    Parameters:
    - a: First number
    - b: Second number
    
    Returns:
    - JSON object with the result of the division operation.
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Both 'a' and 'b' must be valid numbers")
    if b == 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="You cannot divide by zero. Please provide a non-zero value for 'b.'")
    return {"operation": "division", "a": a, "b": b,"result": a / b}


@app.get("/average/{a}/{b}/{c}/{d}", status_code=200)
def average(a: str, b: str, c: str, d: str):
    """
    Calculates the average of four numbers.
    
    Parameters:
    - a: First number
    - b: Second number
    - c: Third number
    - d: Fourth number
    
    Returns:
    - JSON object with the average of the four numbers.
    """
    try:
        a = float(a)
        b = float(b)
        c = float(c)
        d = float(d)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="All parameters 'a', 'b', 'c', and 'd' must be valid numbers")
    return {"operation": "average", "a": a, "b": b,"c": c, "d": d, "result": (a + b + c + d) / 4}
    

@app.get("/tip/{bill_amount}/{tip_percent}", status_code=200)
def tip_calculator(bill_amount: str, tip_percent: str):
    """
    Calculates the tip and total bill amount based on the bill amount and desired tip percentage.
    
    Parameters:
    - bill_amount: Bill amount
    - tip_percent: Tip percent
    
    Returns:
    - JSON object with the tip and total bill amount.
    """
    try:
        bill_amount = float(bill_amount)
        tip_percent = float(tip_percent)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Both 'bill_amount' and 'tip_percent' must be valid numbers")
    if bill_amount < 0 or tip_percent < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="The 'bill_amount' and 'tip_percent' cannot be negative. Please provide non-negative values for both 'bill_amount' and 'tip_percent'.")
    tip_amount = bill_amount * (tip_percent / 100)
    total_bill = bill_amount + tip_amount
    return {"operation": "tip calculation", "Provided bill amount": bill_amount, "Desired tip percent": tip_percent, "tip amount": tip_amount, "total bill amount": total_bill}


@app.get("/percentage/{part}/{whole}", status_code=200)
def percentage(part: str, whole: str):
    """
    Calculate what percent the 'part' is of the 'whole.'
    
    Parameters:
    - part: Part value
    - whole: Whole value
    
    Returns:
    - JSON object with the percentage.
    """
    try:
        part = float(part)
        whole = float(whole)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Both 'part' and 'whole' must be valid numbers")
    if whole == 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="The 'whole' cannot be zero. Please provide a non-zero value for 'b.'")
    return {"operation": "percentage", "part": part, "whole": whole,"result": ((part / whole) * 100)}


@app.get("/dbwritetest", status_code=200)
def dbwritetest(bq: bigquery.Client = Depends(get_bq_client)):
    """
    Writes a simple test row to a BigQuery table.

    Uses the `get_bq_client` dependency method to establish a connection to BigQuery.
    """
    # Define a Python list of objects that will become rows in the database table
    # In this instance, there is only a single object in the list
    row_to_insert = [
        {
            "endpoint": "/dbwritetest",
            "result": "Success",
            "status_code": 200
        }
    ]
    
    # Use the BigQuery interface to write our data to the table
    # If there are errors, store them in a list called `errors`
    # YOU MUST UPDATE YOUR PROJECT AND DATASET NAME BELOW BEFORE THIS WILL WORK!!!
    errors = bq.insert_rows_json("mgmt-467-project-1.calculator.api_logs", row_to_insert)

    # If there were any errors, raise an HTTPException to inform the user
    if errors:
        # Log the full error to your Cloud Run logs for debugging
        print(f"BigQuery Insert Errors: {errors}")
        
        # Raise an exception to the API user
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to log data to BigQuery",
                "errors": errors  # Optional: return specific BQ error details
            }
        )

    # If there were NOT any errors, send a friendly response message to the API caller
    return {"message": "Log entry created successfully"}