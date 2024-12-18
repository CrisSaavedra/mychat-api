from fastapi import APIRouter, Depends
from supabase import Client
from db.connection import get_supabase
import bcrypt

#--- do in another file ---
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password_hash: str
    
#--------------------------


AuthRouter = APIRouter()

@AuthRouter.post("/register")
async def register(new_user: User ,supabase: Client = Depends(get_supabase)):
    hashed_password = bcrypt.hashpw(new_user.password_hash.encode('utf-8'), bcrypt.gensalt())
    new_user.password_hash = hashed_password.decode('utf-8')
    response = (supabase.table('users').insert(new_user.model_dump()).execute())
    return response
