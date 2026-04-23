from pydantic_settings import BaseSettings

# here we are using pydantic's BaseSettings to manage our application settings. 
# This allows us to easily read configuration values from environment variables or a .env file. 
# We can define our database connection details and other settings in this class, and then create an instance of it to access those settings throughout our application.
class Settings(BaseSettings):
    # database_url: str
    # secret_key: str
    # algorithm: str
    # access_token_expire_minutes: int

    # class Config:
    #     env_file = ".env"
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
    

settings = Settings()