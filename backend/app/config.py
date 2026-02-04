from pydantic import BaseModel


class Settings(BaseModel):
    project_name: str = "M&A Thesis Thinking Assistant"
    api_prefix: str = "/api"
    chroma_path: str = "./chroma_data"


settings = Settings()
