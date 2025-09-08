import os
import sys
import logging
import boto3
import psycopg2
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -------------------------------
# Logging
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

# -------------------------------
# Database Configuration
# -------------------------------
DATABASE_URL = os.getenv('DATABASE_URL') or (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

# -------------------------------
# Redis Configuration
# -------------------------------
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

# -------------------------------
# SQS / ElasticMQ Configuration
# -------------------------------
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

QUEUE_URL = os.getenv('SQS_QUEUE_URL')  # full URL including account ID
DLQ_URL = os.getenv('SQS_DLQ_URL')      # full URL including account ID
QUEUE_NAME = os.getenv('SQS_QUEUE_NAME')
DLQ_NAME = os.getenv('SQS_DLQ_NAME')

# Initialize SQS client
sqs_config = {
    'region_name': AWS_REGION,
    'endpoint_url': QUEUE_URL
}

# Add credentials for local ElasticMQ
if 'elasticmq' in QUEUE_URL:
    sqs_config.update({
        'aws_access_key_id': AWS_ACCESS_KEY_ID,
        'aws_secret_access_key': AWS_SECRET_ACCESS_KEY
    })

sqs = boto3.client('sqs', **sqs_config)

# -------------------------------
# Initialization Functions
# -------------------------------
def ensure_sqs_queue():
    try:
        sqs.get_queue_attributes(QueueUrl=QUEUE_URL, AttributeNames=['QueueArn'])
        logger.info("SQS queue access verified.")
    except Exception as e:
        logger.error(f"Error accessing SQS queue: {e}")
        sys.exit(1)

def ensure_db_table():
    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            port=int(os.getenv('POSTGRES_PORT')),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                due_date TIMESTAMP,
                priority VARCHAR(50) DEFAULT 'medium',
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Database table 'todos' ensured.")
    except Exception as e:
        logger.error(f"Error ensuring DB table: {e}")
        sys.exit(1)

def ensure_redis():
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
        r.ping()
        logger.info("Redis connection ensured.")
    except Exception as e:
        logger.error(f"Error ensuring Redis: {e}")
        sys.exit(1)

def initialize_services():
    logger.info("Initializing services...")
    ensure_sqs_queue()
    ensure_db_table()
    ensure_redis()
    logger.info("All services initialized successfully.")
