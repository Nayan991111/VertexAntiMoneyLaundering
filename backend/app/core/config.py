from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "VertexAntiMoneyLaundering Compliance Engine"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # DATABASE (Matches docker-compose services: db)
    POSTGRES_USER: str = "sentinelflow"
    POSTGRES_PASSWORD: str = "securepassword"
    POSTGRES_DB: str = "compliance_db"
    POSTGRES_HOST: str = "db"
    
    # DATABASE_URL: We construct it explicitly if not in ENV
    DATABASE_URL: Optional[str] = None

    # GRAPH (Matches docker-compose services: neo4j)
    NEO4J_URI: str = "bolt://neo4j:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "securegraphpass"

    # Day 10: Active Intervention
    ALERT_THRESHOLD_SCORE: int = 80
    ENABLE_EMAIL_NOTIFICATIONS: bool = True
    AUDIT_LOG_PATH: str = "/app/logs/audit_trail.jsonl"
    COMPLIANCE_OFFICER_EMAIL: str = "officer@sentinelflow.com"

    # Pydantic V2: Construct the URL after initialization if missing
    def model_post_init(self, __context):
        if not self.DATABASE_URL:
            # Note: We use postgresql+asyncpg for SQLAlchemy async engine
            self.DATABASE_URL = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        # Ignores extra env vars to prevent crashes
        extra = "ignore" 

settings = Settings()