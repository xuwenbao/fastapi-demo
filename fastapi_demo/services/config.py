import platform
from pathlib import Path
from functools import lru_cache

import yaml
from loguru import logger
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

THIS_DIR = Path(__file__).parent
ENV_FILE = Path(THIS_DIR, "../../.env")
# TODO: 配置文件路径未测试
CONFIG_FILES = [
    Path("C:\\config.yml") if platform.system() == "Windows" else Path("~/.config.yml").expanduser(),
    Path(THIS_DIR, "../config.yml"),
    Path(THIS_DIR, "../config/config.yml"),
]


class Mysql(BaseModel):
    host: str = Field(default="127.0.0.1", required=True)
    port: int = Field(default=3306, required=True)
    db: str = Field(default="demo", required=True)
    username: str = Field(default="root", required=True)
    password: str = Field(default="1234", required=True)

    @property
    def database_url(self):
        return f"mysql+aiomysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='CHANGEME_', env_file=ENV_FILE.resolve(),
                                      env_nested_delimiter='__') # 以双下划线作为嵌套分隔符
    
    testing: bool = Field(default=False)
    mysql: Mysql = Field(default_factory=Mysql, required=True)

    @staticmethod
    def load() -> "AppSettings":
        # 依次从配置文件列表中，按优先级读取配置文件。
        # 如果未找到配置文件，则返回默认配置。
        for path in CONFIG_FILES:
            if not path.is_file():
                logger.debug(f"未发现配置文件在：`{path.resolve()}`")
                continue

            logger.info(f"读取配置文件从： `{path.resolve()}`")
            with open(path, "r", encoding='utf8') as yaml_file:
                config_data = yaml.safe_load(yaml_file)
                s = AppSettings(**config_data)
                return s
        else:
            return AppSettings()


@lru_cache()
def get_settings() -> AppSettings:
    settings = AppSettings.load()

    if ENV_FILE.exists():
        logger.debug(f'env_file: {ENV_FILE.resolve()}')

    logger.info(f'============================================================')
    logger.info(f'settings: ')
    logger.info(f'testing: {settings.testing}')

    logger.info(f'mysql host: {settings.mysql.host}')
    logger.info(f'mysql port: {settings.mysql.port}')
    logger.info(f'mysql database: {settings.mysql.db}')
    logger.info(f'mysql user: {settings.mysql.username}')
    logger.info(f'mysql password: {settings.mysql.password}')
    logger.info(f'============================================================')

    return settings