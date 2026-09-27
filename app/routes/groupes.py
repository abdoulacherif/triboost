from fastapi import APIRouter, HTTPException

# ⚠️ Adapte cet import à l'endroit où tu initialises ton client Supabase
# (le même que celui utilisé par app/routes/auth.py)
from app.supabase_client import supabase

router = APIRouter()


@router.get("")
async def get_groupes():
    try:
        response = (
            supabase.table("groupes")
            .select("id, name, description, link")
            .order("created_at")
            .execute()
        )
        return {"groupes": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
