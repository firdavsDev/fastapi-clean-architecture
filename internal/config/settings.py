import os
from typing import Any, Dict, List, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


def get_env_file(env_file: str):
    if os.getenv('LEVEL') == 'debug':
        return env_file.format('example.env')
    return env_file.format('.env')


class Settings(BaseSettings):

    API: str = '/api'
    ADMIN: str = '/admin'
    STARTUP: str = 'startup'
    SECRET_KEY: str
    FLASK_ADMIN_SWATCH: str = 'cerulean'

    PROJECT_NAME: str = 'FastAPI'
    DESCRIPTION: str = 'FastAPI clean architecture'

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(
        cls, value: Union[str, List[str]]  # noqa: N805
    ) -> Union[List[str], str]:
        if isinstance(value, str) and not value.startswith('['):
            return [i.strip() for i in value.split(',')]
        elif isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(
        cls, value: str | None, values: Dict[str, Any]  # noqa: N805
    ) -> str:
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('DB_USER'),
            password=values.get('DB_PASSWORD'),
            host=values.get('DB_HOST'),
            port=values.get('DB_PORT'),
            path='/{0}'.format(values.get('DB_NAME')),
        )

    class Config(object):
        case_sensitive = True
        env_file = get_env_file('env/{0}')


settings = Settings()