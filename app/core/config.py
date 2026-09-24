import os


class Settings:
    # ... existant ...

    # LeekPay
    LEEKPAY_PUBLIC_KEY: str = os.environ.get("LEEKPAY_PUBLIC_KEY", "")
    LEEKPAY_SECRET_KEY: str = os.environ.get("LEEKPAY_SECRET_KEY", "")
    LEEKPAY_API_URL: str = os.environ.get("LEEKPAY_API_URL", "https://leekpay.fr/api/v1")
    LEEKPAY_WEBHOOK_SECRET: str = os.environ.get("LEEKPAY_WEBHOOK_SECRET", "")

    @property
    def is_leekpay_configured(self) -> bool:
        return bool(self.LEEKPAY_SECRET_KEY and self.LEEKPAY_API_URL)


settings = Settings()