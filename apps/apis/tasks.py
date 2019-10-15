from celery import shared_task
from celery.utils.log import get_task_logger
from .utils import *
from config.celery_app import app

logger = get_task_logger(__name__)


@shared_task
def sample_task(par1, par2):
    logger.info(par1, par2)
