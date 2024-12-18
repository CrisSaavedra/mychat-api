from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from db.connection import get_supabase
import bcrypt

#--- do in another file ---
from pydantic import BaseModel

class User(BaseModel):
    email: str
    password_hash: str
    username: str | None = None
    
#--------------------------


AuthRouter = APIRouter()

# @AuthRouter.post("/register")
# async def register(new_user: User ,supabase: Client = Depends(get_supabase)):
#     hashed_password = bcrypt.hashpw(new_user.password_hash.encode('utf-8'), bcrypt.gensalt())
#     new_user.password_hash = hashed_password.decode('utf-8')
#     response = supabase.table('users').insert(new_user.model_dump()).execute()
#     return response

@AuthRouter.post("/register")
async def register(new_user: User, supabase: Client = Depends(get_supabase)):
    try:
        hashed_password = bcrypt.hashpw(new_user.password_hash.encode('utf-8'), bcrypt.gensalt())
        new_user.password_hash = hashed_password.decode('utf-8')

        response = supabase.table('users').insert(new_user.model_dump()).execute()
        
        if 'error' in response:
            raise HTTPException(status_code=400, detail="Failed to create user")
        
        return {"message": "User created successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@AuthRouter.post("/login")
async def login(user: User, supabase: Client = Depends(get_supabase)):
    response = supabase.table('users').select('*').eq('email', user.email).execute()
    
    # Comprueba si se encontró el usuario y si hay datos en la respuesta
    if not response.data:
        return {"message": "Invalid credentials"}
    
    # Obtén el hash almacenado y verifica la contraseña
    stored_password_hash = response.data[0]['password_hash'].encode('utf-8')
    if bcrypt.checkpw(user.password_hash.encode('utf-8'), stored_password_hash):
        return {"message": "Logged in successfully"}
    else:
        return {"message": "Invalid credentials"}
