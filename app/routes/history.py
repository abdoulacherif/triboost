from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


# ============================================================
# HISTORIQUE COMPLET + STATS POUR GRAPHIQUES
# ============================================================
@router.get("/")
async def get_history(request: Request):
    """Retourne l'historique complet + statistiques pour graphiques."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")

        # 1️⃣ Vérifier l'utilisateur
        supabase_anon = get_supabase()
        user_response = supabase_anon.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        user_id = user_response.user.id
        admin = get_supabase_admin()

        # 2️⃣ Récupérer les commissions
        commissions_result = (
            admin.table("commissions")
            .select("id, level, amount, description, created_at, from_user_id")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(200)
            .execute()
        )
        commissions = commissions_result.data or []

        # 3️⃣ Récupérer les activations
        activations_result = (
            admin.table("activations")
            .select("id, amount, payment_method, payment_reference, status, created_at, completed_at")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(100)
            .execute()
        )
        activations = activations_result.data or []

        # 4️⃣ Calculer les stats pour les graphiques
        now = datetime.now(timezone.utc)

        # Gains par jour (7 derniers jours)
        daily = {}
        for i in range(6, -1, -1):
            d = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            daily[d] = 0

        # Gains par semaine (4 dernières semaines)
        weekly = {}
        for i in range(3, -1, -1):
            # Lundi de la semaine
            monday = now - timedelta(days=now.weekday() + i * 7)
            key = monday.strftime("%Y-W%V")
            weekly[key] = 0

        # Gains par mois (6 derniers mois)
        monthly = {}
        for i in range(5, -1, -1):
            # Approximation : mois - i
            month_date = now.replace(day=1)
            for _ in range(i):
                month_date = (month_date - timedelta(days=1)).replace(day=1)
            key = month_date.strftime("%Y-%m")
            monthly[key] = 0

        # Remplir les données
        total_gains = 0
        for c in commissions:
            amount = float(c.get("amount", 0))
            total_gains += amount
            try:
                dt = datetime.fromisoformat(c["created_at"].replace("Z", "+00:00"))
                day_key = dt.strftime("%Y-%m-%d")
                week_key = dt.strftime("%Y-W%V")
                month_key = dt.strftime("%Y-%m")

                if day_key in daily:
                    daily[day_key] += amount
                if week_key in weekly:
                    weekly[week_key] += amount
                if month_key in monthly:
                    monthly[month_key] += amount
            except Exception:
                pass

        # 5️⃣ Répartition par niveau
        level_stats = {"n1": 0, "n2": 0, "n3": 0}
        level_counts = {"n1": 0, "n2": 0, "n3": 0}
        for c in commissions:
            level = c.get("level")
            amount = float(c.get("amount", 0))
            if level == 1:
                level_stats["n1"] += amount
                level_counts["n1"] += 1
            elif level == 2:
                level_stats["n2"] += amount
                level_counts["n2"] += 1
            elif level == 3:
                level_stats["n3"] += amount
                level_counts["n3"] += 1

        return {
            "success": True,
            "commissions": commissions,
            "activations": activations,
            "stats": {
                "total_gains": total_gains,
                "total_commissions": len(commissions),
                "level_stats": level_stats,
                "level_counts": level_counts,
                "daily": daily,
                "weekly": weekly,
                "monthly": monthly,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[HISTORY] Erreur: {e}")
        raise HTTPException(status_code=400, detail=str(e))