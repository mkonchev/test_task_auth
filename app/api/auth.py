from fastapi import APIRouter

authRouter = APIRouter()


@authRouter.post("/register")
async def register():
    return {"data": "register"}


@authRouter.post("/login")
async def login():
    return {"data": "login"}


@authRouter.post("/logout")
async def logout():
    return {"data": "success"}


@authRouter.patch("/update")
async def update():
    return {"data": "success"}


@authRouter.patch("/delete")
async def delete():
    return {"data": "success"}
