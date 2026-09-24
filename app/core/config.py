import os


class Settings:
    """Configuration centralisée de TriBoost."""

    # ===== App =====
    APP_NAME: str = "TriBoost"
    BASE_URL: str = os.environ.get("BASE_URL", "https://triboost.vercel.app")

    # ===== Supabase =====
    SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.environ.get("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

    # ===== LeekPay =====
    LEEKPAY_PUBLIC_KEY: str = os.environ.get("LEEKPAY_PUBLIC_KEY", "")
    LEEKPAY_SECRET_KEY: str = os.environ.get("LEEKPAY_SECRET_KEY", "")
    LEEKPAY_API_URL: str = os.environ.get(
        "LEEKPAY_API_URL", "https://leekpay.fr/api/v1"
    )

    # ===== Vérifications =====
    @property
    def is_configured(self) -> bool:
        """Supabase est-il configuré ?"""
        return bool(self.SUPABASE_URL and self.SUPABASE_ANON_KEY)

    @property
    def is_admin_configured(self) -> bool:
        """Supabase service_role est-elle configurée ?"""
        return bool(self.SUPABASE_URL and self.SUPABASE_SERVICE_ROLE_KEY)

    @property
    def is_leekpay_configured(self) -> bool:
        """LeekPay est-il configuré ?"""
        return bool(self.LEEKPAY_SECRET_KEY and self.LEEKPAY_API_URL)


settings = Settings()