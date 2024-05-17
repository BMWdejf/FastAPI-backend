from app.db.base import supabase

def products():
    return supabase.table("products").select("*").execute()