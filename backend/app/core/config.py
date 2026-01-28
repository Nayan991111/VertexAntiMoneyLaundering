from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Project Metadata
    PROJECT_NAME: str = "ZeTheta Regulatory Compliance Engine"
    PROJECT_VERSION: str = "0.1.0"
    
    # Database Configuration
    DATABASE_URL: str = "postgresql+asyncpg://admin:secure_password_123@localhost:5432/compliance_db"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "secure_graph_pass_123"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()