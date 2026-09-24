from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


# ============================================================
# LISTER LES FORMATIONS
# ============================================================
@router.get("/")
async def list_formations(
    category: str | None = None,
    search: str | None = None,
):
    """Liste toutes les formations publiées."""
    try:
        admin = get_supabase_admin()
        query = (
            admin.table("formations")
            .select("id, title, description, category, cover_url, duration, level, price, is_free, author, views, created_at")
            .eq("is_published", True)
            .order("created_at", desc=True)
        )

        if category and category != "tous":
            query = query.eq("category", category)

        result = query.execute()
        items = result.data or []

        if search:
            s = search.lower()
            items = [
                i for i in items
                if s in (i.get("title", "") or "").lower()
                or s in (i.get("description", "") or "").lower()
            ]

        return {"success": True, "formations": items, "count": len(items)}
    except Exception as e:
        print(f"[FORMATIONS] Erreur list: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# DÉTAIL D'UNE FORMATION
# ============================================================
@router.get("/{formation_id}")
async def get_formation(formation_id: str, request: Request):
    """Retourne une formation + statut d'achat de l'utilisateur."""
    try:
        admin = get_supabase_admin()

        # Récupérer la formation
        result = (
            admin.table("formations")
            .select("*")
            .eq("id", formation_id)
            .eq("is_published", True)
            .execute()
        )

        if not result.data or len(result.data) == 0:
            raise HTTPException(status_code=404, detail="Formation introuvable")

        formation = result.data[0]

        # Incrémenter les vues
        try:
            admin.table("formations").update({
                "views": (formation.get("views") or 0) + 1
            }).eq("id", formation_id).execute()
        except Exception:
            pass

        # Statut d'achat (si utilisateur connecté)
        has_access = formation.get("is_free", True)
        user_id = None

        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
            try:
                supabase_anon = get_supabase()
                user = supabase_anon.auth.get_user(token)
                if user.user:
                    user_id = user.user.id
                    check = (
                        admin.table("formation_purchases")
                        .select("id")
                        .eq("user_id", user_id)
                        .eq("formation_id", formation_id)
                        .execute()
                    )
                    if check.data and len(check.data) > 0:
                        has_access = True
            except Exception:
                pass

        # Ne pas exposer le contenu si pas d'accès
        response_formation = dict(formation)
        if not has_access:
            response_formation["content_url"] = None
            response_formation["content_text"] = None

        return {
            "success": True,
            "formation": response_formation,
            "has_access": has_access,
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[FORMATIONS] Erreur detail: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# ACHETER UNE FORMATION
# ============================================================
@router.post("/{formation_id}/purchase")
async def purchase_formation(formation_id: str, request: Request):
    """Achète une formation (débit du wallet si payante)."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")

        supabase_anon = get_supabase()
        user_response = supabase_anon.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        user_id = user_response.user.id

        admin = get_supabase_admin()
        result = admin.rpc(
            "purchase_formation",
            {
                "p_user_id": user_id,
                "p_formation_id": formation_id,
            }
        ).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Échec de l'achat")

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[FORMATIONS] Erreur purchase: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# MES FORMATIONS ACHETÉES
# ============================================================
@router.get("/me/purchases")
async def my_purchases(request: Request):
    """Retourne les formations achetées par l'utilisateur."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")

        supabase_anon = get_supabase()
        user_response = supabase_anon.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        user_id = user_response.user.id
        admin = get_supabase_admin()

        result = (
            admin.table("formation_purchases")
            .select("formation_id, amount, created_at, formations(id, title, cover_url, category, duration)")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

        return {"success": True, "purchases": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[FORMATIONS] Erreur purchases: {e}")
        raise HTTPException(status_code=400, detail=str(e))