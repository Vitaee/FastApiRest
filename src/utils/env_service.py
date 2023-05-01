from dotenv import load_dotenv
from pathlib import Path
import os


class EnvService:
    def __init__(self):
        pass        

    def load_env(self, env):
        env_path = f".env.{env}"
        env_file = Path(env_path)

        if env_file.exists():
            load_dotenv(dotenv_path=env_file)
        else:
            raise ValueError(f"Environment file not found: {env_path}")

        # Define required environment variables
        self.required_env_vars = [
            "DB_URL",
            # Add more required variables here
        ]

        # Check if required environment variables are defined
        missing_vars = [var for var in self.required_env_vars if var not in os.environ]
        if missing_vars:
            raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

    def get_env_var(self, var_name: str) -> str:
        return os.environ[var_name]

env_service = EnvService()