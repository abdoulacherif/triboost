from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


# ============================================================
# ⚠️ ORDRE IMPORTANT : les routes statiques AVANT /{formation_id}
# ============================================================


# ============================================================
# LISTER LES FORMATIONS
# ============================================================
@router.get("/")
async def list_formations(
    category: str | None = None,
    search: str | None = None,
):
    try:
        admin = get_supabase_admin()
        query = (
            admin.table("formations")
            .select("id, title, description, category, cover_url, duration, level, price, is_free, author, views, created_at")
            .eq("is_published", True)
            .order("created_at", desc=True)
            .limit(100)
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
# ROUTES STATIQUES — DOIVENT ÊTRE AVANT /{formation_id}
# ============================================================

# 1. PARCOURS — LISTE
@router.get("/paths")
async def list_paths(request: Request):
    try:
        admin = get_supabase_admin()
        paths_result = admin.table("paths").select("*").eq("is_active", True).order("sort_order").execute()
        paths = paths_result.data or []

        for p in paths:
            pf = admin.table("path_formations").select(
                "formation_id, sort_order, formations(id, title, cover_url, category, duration, is_free, price)"
            ).eq("path_id", p["id"]).order("sort_order").execute()
            p["formations"] = [item.get("formations") for item in (pf.data or []) if item.get("formations")]
            p["total_formations"] = len(p["formations"])

        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
            try:
                user = get_supabase().auth.get_user(token)
                if user.user:
                    prog = admin.table("path_progress").select("path_id, formation_id").eq("user_id", user.user.id).execute()
                    progress_map = {}
                    for item in (prog.data or []):
                        pid = item["path_id"]
                        if pid not in progress_map:
                            progress_map[pid] = []
                        progress_map[pid].append(item["formation_id"])

                    for p in paths:
                        done_ids = progress_map.get(p["id"], [])
                        p["completed_ids"] = done_ids
                        p["completed_count"] = len(done_ids)
                        p["is_completed"] = p["completed_count"] >= p["total_formations"] and p["total_formations"] > 0
            except Exception:
                pass

        return {"success": True, "paths": paths}
    except Exception as e:
        print(f"[FORMATIONS] Erreur paths: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# 2. PARCOURS — DÉTAIL
@router.get("/paths/{path_id}")
async def get_path(path_id: str, request: Request):
    try:
        admin = get_supabase_admin()
        path = admin.table("paths").select("*").eq("id", path_id).eq("is_active", True).execute()
        if not path.data or len(path.data) == 0:
            raise HTTPException(status_code=404, detail="Parcours introuvable")

        p = path.data[0]
        pf = admin.table("path_formations").select("formation_id, sort_order, formations(*)").eq("path_id", path_id).order("sort_order").execute()
        p["formations"] = [item.get("formations") for item in (pf.data or []) if item.get("formations")]

        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
            try:
                user = get_supabase().auth.get_user(token)
                if user.user:
                    prog = admin.table("path_progress").select("formation_id").eq("user_id", user.user.id).eq("path_id", path_id).execute()
                    done_ids = [item["formation_id"] for item in (prog.data or [])]
                    p["completed_ids"] = done_ids
                    p["completed_count"] = len(done_ids)
                    p["is_completed"] = p["completed_count"] >= len(p["formations"]) and len(p["formations"]) > 0
            except Exception:
                pass

        return {"success": True, "path": p}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 3. MES ACHATS
@router.get("/me/purchases")
async def my_purchases(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        supabase_anon = get_supabase()
        user_response = supabase_anon.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        result = (
            admin.table("formation_purchases")
            .select("formation_id, amount, created_at, formations(id, title, cover_url, category, duration)")
            .eq("user_id", user_response.user.id)
            .order("created_at", desc=True)
            .execute()
        )
        return {"success": True, "purchases": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 4. MES CERTIFICATS
@router.get("/certificates")
async def my_certificates(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        result = admin.table("certificates").select("*").eq("user_id", user.user.id).order("created_at", desc=True).execute()
        return {"success": True, "certificates": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# ROUTES DYNAMIQUES — À METTRE EN DERNIER
# ============================================================

# 5. COMPLÉTER UNE FORMATION
@router.post("/complete/{formation_id}")
async def complete_formation(formation_id: str, request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        user_id = user.user.id
        admin = get_supabase_admin()

        profile = admin.table("profiles").select("is_activated").eq("id", user_id).execute()
        raw = profile.data[0].get("is_activated") if profile.data else False
        is_activated = raw is True or raw == "true" or raw == 1 or raw == "1"
        if not is_activated:
            raise HTTPException(status_code=403, detail="Compte non activé")

        result = admin.rpc("complete_formation", {
            "p_user_id": user_id,
            "p_formation_id": formation_id,
        }).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Erreur")

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 6. ACHETER UNE FORMATION
@router.post("/{formation_id}/purchase")
async def purchase_formation(formation_id: str, request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        supabase_anon = get_supabase()
        user_response = supabase_anon.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        result = admin.rpc(
            "purchase_formation",
            {
                "p_user_id": user_response.user.id,
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


# 7. DÉTAIL D'UNE FORMATION (⚠️ DOIT ÊTRE EN DERNIER)
@router.get("/{formation_id}")
async def get_formation(formation_id: str, request: Request):
    try:
        admin = get_supabase_admin()

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

        try:
            admin.table("formations").update({
                "views": (formation.get("views") or 0) + 1
            }).eq("id", formation_id).execute()
        except Exception:
            pass

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