from fastapi import FastAPI, HTTPException, Query

import db
import api

app = FastAPI()

db.init_db()


@app.get("/unit")
def read_unit_info(name: str = Query()):
    """Returns response json with unit info"""
    return api.get_unit(name)


@app.get("/stack")
def read_stack_info(name: str = Query(), size: int = Query(default=1)):
    """Returns response json with stack of units info"""
    if size <= 0:
        raise HTTPException(status_code=400, detail="Size must be greater than there")
    return api.calculate_stack(name, size)
