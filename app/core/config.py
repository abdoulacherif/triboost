import os


class Settings:
    """Configuration centralisée."""
    APP_NAME: str = "TriBoost"
    SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.environ.get("SUPABASE_ANON_KEY", "")

    @property
    def is_configured(self) -> bool:
        return bool(self.SUPABASE_URL and self.SUPABASE_ANON_KEY)


settings = Settings()