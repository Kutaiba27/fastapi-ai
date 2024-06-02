


from typing import Annotated

from fastapi import HTTPException, Header


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "hello":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "hello1":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key
