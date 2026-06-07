import logging
from datetime import datetime

from network_security.config.settings import get_settings


settings = get_settings()
settings.paths.log_dir.mkdir(parents=True, exist_ok=True)

LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = settings.paths.log_dir / LOG_FILE

logging.basicConfig(
    filename=str(LOG_FILE_PATH),
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, settings.log_level, logging.INFO),
)
