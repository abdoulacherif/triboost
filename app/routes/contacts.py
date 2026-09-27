from fastapi import APIRouter, HTTPException

# ⚠️ Adapte cet import à l'endroit où tu initialises ton client Supabase
# (le même que celui utilisé par app/routes/auth.py)
from app.supabase_client import supabase

router = APIRouter()


@router.get("")
async def get_contacts():
    try:
        response = (
            supabase.table("contacts")
            .select("id, name, role, phone")
            .order("created_at")
            .execute()
        )
        return {"contacts": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
