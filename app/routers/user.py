from fastapi import APIRouter, Depends
from supabase import Client
from db.connection import get_supabase

UserRouter = APIRouter()

@UserRouter.get("/")
async def root():
    return {"message": "Hello Worlds"}

@UserRouter.get("/all")
async def get_all_users( supabase: Client = Depends(get_supabase)):
    return supabase.table("users").select("*").execute()