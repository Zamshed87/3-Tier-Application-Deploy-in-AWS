import os
import boto3
import time
import logging
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis

logger = logging.getLogger("config")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

Base = declarative_base()

# SQS config
QUEUE_URL = os.getenv('SQS_QUEUE_URL')
DLQ_URL = os.getenv('SQS_DLQ_URL')

sqs_config = {
    'region_name': os.getenv('AWS_REGION', 'us-east-1'),
    'endpoint_url': QUEUE_URL
}

if 'elasticmq' in QUEUE_URL:
    sqs_config.update({
        'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID', 'x'),
        'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY', 'x')
    })

sqs = boto3.client('sqs', **sqs_config)

# Database
DB_URI = os.getenv('DATABASE_URI', 'postgresql://postgres:postgres@db:5432/todos')
engine = create_engine(DB_URI)
SessionLocal = sessionmaker(bind=engine)

# Redis
redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=int(os.getenv('REDIS_PORT', 6379)), db=0)

# Models
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    status = Column(String(50), default="pending")

# Ensure DB table
def ensure_db_table():
    for i in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database table 'todos' ensured.")
            return
        except Exception as e:
            logger.warning(f"DB not ready yet ({i+1}/10): {e}")
            time.sleep(2)
    logger.error("DB could not be reached. Exiting.")
    raise Exception("Database not ready")

# Ensure Redis
def ensure_redis():
    for i in range(10):
        try:
            redis_client.ping()
            logger.info("Redis connection ensured.")
            return
        except Exception as e:
            logger.warning(f"Redis not ready yet ({i+1}/10): {e}")
            time.sleep(2)
    logger.error("Redis could not be reached. Exiting.")
    raise Exception("Redis not ready")

# Ensure SQS queue
def ensure_sqs_queue():
    for i in range(10):
        try:
            sqs.get_queue_attributes(QueueUrl=QUEUE_URL, AttributeNames=['QueueArn'])
            logger.info("SQS queue access verified.")
            return
        except Exception as e:
            logger.warning(f"SQS not ready yet ({i+1}/10): {e}")
            time.sleep(2)
    logger.error("SQS could not be reached. Exiting.")
    raise Exception("SQS not ready")

def initialize_services():
    logger.info("Initializing services...")
    ensure_sqs_queue()
    ensure_db_table()
    ensure_redis()
    logger.info("All services initialized successfully.")
