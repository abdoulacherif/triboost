from fastapi import APIRouter, HTTPException, Request

from app.core.supabase_client import get_supabase, get_supabase_admin

router = APIRouter()


# ============================================================
# LISTE DES FILLEULS (pour choisir à qui envoyer)
# ============================================================
@router.get("/contacts")
async def get_contacts(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()

        # Récupérer tous mes filleuls directs
        result = admin.table("profiles").select(
            "id, full_name, phone, is_activated, referral_code"
        ).eq("referred_by", user.user.id).order("created_at", desc=True).execute()

        contacts = result.data or []

        # Ajouter les infos de dernier message
        for c in contacts:
            try:
                last = admin.table("chat_messages").select(
                    "message, created_at, sender_id"
                ).or_(
                    f"and(sender_id.eq.{user.user.id},receiver_id.eq.{c['id']}),and(sender_id.eq.{c['id']},receiver_id.eq.{user.user.id})"
                ).order("created_at", desc=True).limit(1).execute()
                if last.data and len(last.data) > 0:
                    c["last_message"] = last.data[0]["message"]
                    c["last_date"] = last.data[0]["created_at"]
            except Exception:
                pass

        return {"success": True, "contacts": contacts}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[CHAT] contacts: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# CONVERSATION AVEC UN CONTACT
# ============================================================
@router.get("/conversation/{contact_id}")
async def get_conversation(contact_id: str, request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()

        # Récupérer les messages des deux côtés
        sent = admin.table("chat_messages").select("*").eq("sender_id", user.user.id).eq("receiver_id", contact_id).execute()
        received = admin.table("chat_messages").select("*").eq("sender_id", contact_id).eq("receiver_id", user.user.id).execute()

        messages = (sent.data or []) + (received.data or [])
        messages.sort(key=lambda m: m.get("created_at", ""))

        # Marquer comme lus
        try:
            admin.table("chat_messages").update({"is_read": True}).eq("sender_id", contact_id).eq("receiver_id", user.user.id).execute()
        except Exception:
            pass

        # Infos contact
        contact = admin.table("profiles").select("id, full_name, phone, is_activated").eq("id", contact_id).execute()

        return {
            "success": True,
            "messages": messages,
            "contact": contact.data[0] if contact.data else None,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# ENVOYER UN MESSAGE
# ============================================================
@router.post("/send")
async def send_message(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        body = await request.json()
        receiver_id = body.get("receiver_id")
        message = (body.get("message") or "").strip()

        if not receiver_id:
            raise HTTPException(status_code=400, detail="Destinataire obligatoire")
        if not message:
            raise HTTPException(status_code=400, detail="Message vide")

        admin = get_supabase_admin()

        # Vérifier que le destinataire est bien un filleul
        check = admin.table("profiles").select("id, referred_by").eq("id", receiver_id).execute()
        if not check.data:
            raise HTTPException(status_code=404, detail="Contact introuvable")

        is_my_filleul = check.data[0].get("referred_by") == user.user.id

        if not is_my_filleul:
            raise HTTPException(status_code=403, detail="Tu ne peux envoyer qu'à tes filleuls")

        result = admin.table("chat_messages").insert({
            "sender_id": user.user.id,
            "receiver_id": receiver_id,
            "message": message,
        }).execute()

        return {"success": True, "message": result.data[0] if result.data else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# MESSAGES NON LUS
# ============================================================
@router.get("/unread")
async def unread_count(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        result = admin.table("chat_messages").select("id").eq("receiver_id", user.user.id).eq("is_read", False).execute()

        return {"success": True, "unread": len(result.data or [])}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# SUPPORT — MES TICKETS
# ============================================================
@router.get("/support/tickets")
async def my_tickets(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        admin = get_supabase_admin()
        result = admin.table("support_tickets").select("*").eq("user_id", user.user.id).order("created_at", desc=True).execute()

        return {"success": True, "tickets": result.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# SUPPORT — CRÉER UN TICKET
# ============================================================
@router.post("/support/tickets")
async def create_ticket(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")

        token = auth_header.replace("Bearer ", "")
        user = get_supabase().auth.get_user(token)
        if not user.user:
            raise HTTPException(status_code=401, detail="Token invalide")

        body = await request.json()
        subject = (body.get("subject") or "").strip()
        message = (body.get("message") or "").strip()

        if not subject or not message:
            raise HTTPException(status_code=400, detail="Sujet et message obligatoires")

        admin = get_supabase_admin()
        result = admin.table("support_tickets").insert({
            "user_id": user.user.id,
            "subject": subject,
            "message": message,
            "status": "open",
        }).execute()

        return {"success": True, "ticket": result.data[0] if result.data else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))