#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from loguru import logger


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dico_event.settings')
    try:
        logger.remove()
        logger.add(sys.stdout, level="INFO")
        LOG_FORMAT = (
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level:<8} | "
            "{name}:{function}:{line} - "
            "{message}"
        )

        logger.add("logs/error.log",
                rotation="1 day",  
                level="ERROR",  
                backtrace=True,
                diagnose=True, 
                format=LOG_FORMAT,
        ) 
        logger.add("logs/application.log",
                rotation="1 day",  
                level="INFO", 
                filter=lambda record: record["level"].name in ("INFO", "WARNING"),
                format=LOG_FORMAT,
        )
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
