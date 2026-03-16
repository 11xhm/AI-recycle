import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _env_bool(name: str, default: bool) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "y", "on"}


class Settings:
    def __init__(self) -> None:
        backend_dir = Path(__file__).resolve().parents[2]
        repo_root = backend_dir.parent

        self.ai_mock: bool = _env_bool("AI_MOCK", True)
        self.ai_provider: str = os.getenv("AI_PROVIDER", "mock").strip().lower()
        self.ai_timeout_seconds: float = float(os.getenv("AI_TIMEOUT_SECONDS", "15"))

        self.baidu_api_key: str = os.getenv("BAIDU_API_KEY", "")
        self.baidu_secret_key: str = os.getenv("BAIDU_SECRET_KEY", "")
        self.baidu_endpoint: str = os.getenv(
            "BAIDU_ENDPOINT", "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
        )
        self.baidu_oauth_endpoint: str = os.getenv("BAIDU_OAUTH_ENDPOINT", "https://aip.baidubce.com/oauth/2.0/token")

        self.pricing_path: Path = Path(os.getenv("PRICING_PATH", str(repo_root / "shared" / "pricing.json"))).resolve()
        self.max_upload_bytes: int = int(os.getenv("MAX_UPLOAD_BYTES", str(8 * 1024 * 1024)))

        self.db_path: Path = Path(os.getenv("DB_PATH", str(repo_root / "shared" / "app.db"))).resolve()

        self.jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret-change-me")
        self.jwt_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "10080"))

        self.upload_dir: Path = Path(os.getenv("UPLOAD_DIR", str(repo_root / "shared" / "uploads"))).resolve()

        origins = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:5173").strip()
        self.cors_allow_origins: list[str] = [o.strip() for o in origins.split(",") if o.strip()]


settings = Settings()
