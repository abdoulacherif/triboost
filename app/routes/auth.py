@router.get("/profile/{user_id}")
async def get_profile(user_id: str, request: Request):
    """Récupère le profil complet d'un utilisateur."""
    try:
        # Vérifier le token
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        supabase = get_supabase()

        # Vérifier l'utilisateur
        user_response = supabase.auth.get_user(token)
        if user_response.user.id != user_id:
            raise HTTPException(status_code=403, detail="Accès refusé")

        # Récupérer le profil
        result = (
            supabase.table("profiles")
            .select("*")
            .eq("id", user_id)
            .single()
            .execute()
        )

        if not result.data:
            raise HTTPException(status_code=404, detail="Profil introuvable")

        return {"success": True, "profile": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/activate")
async def activate(request: Request):
    """Active le compte de l'utilisateur (paiement 3600 FCFA)."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        body = await request.json()
        payment_method = body.get("payment_method", "manual")
        payment_reference = body.get("payment_reference", "")

        supabase = get_supabase()

        # Vérifier l'utilisateur
        user_response = supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        # Activer le compte
        result = supabase.rpc(
            "activate_account",
            {
                "p_user_id": user_response.user.id,
                "p_payment_method": payment_method,
                "p_payment_reference": payment_reference or None,
            }
        ).execute()

        if not result.data:
            raise HTTPException(status_code=400, detail="Échec de l'activation")

        return {"success": True, "result": result.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))