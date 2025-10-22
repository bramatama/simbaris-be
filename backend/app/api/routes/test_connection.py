from fastapi import APIRouter
from app.config.supabase import supabase

router = APIRouter()

@router.get("/test-connection")
async def test_connection():
    try:
        response = supabase.table("schools").select("*").execute()
        return {
            "success": True,
            "count": len(response.data),
            "data": response.data
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
