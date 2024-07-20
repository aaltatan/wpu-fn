import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

import logging


if __name__ == "__main__":
    
    logging.basicConfig(
        filemode='a',
        filename='logger.log',
        format='[%(asctime)s] %(levelname)s | %(name)s => %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8',
        level=logging.INFO
    )
    
    env_path = Path().resolve() / '.env'
    load_dotenv(env_path)
    
    kwargs: dict = {
        'app': 'core.asgi:application',
        'host': int(os.getenv('HOST')) or '127.0.0.1',
        'port': int(os.getenv('PORT')) or 8000,
    }
    
    uvicorn.run(**kwargs)