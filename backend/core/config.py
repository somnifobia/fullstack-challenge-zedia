from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Mensageiro API"
    PROJECT_VERSION: str = "0.1.0"

    DB_USER: str = "mensageiro"
    DB_PASSWORD: str = "mensageiro"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "mensageiro"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
settings = Settings()