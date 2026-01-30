import os
from fastapi import FastAPI, UploadFile, File, HTTPException
import boto3
from botocore.client import Config
import psycopg

APP_NAME = "sticker-api"

def get_db_conn():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "postgres"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "stickers"),
        user=os.getenv("DB_USER", "stickers_user"),
        password=os.getenv("DB_PASSWORD", "stickers_pass"),
    )

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT", "http://minio:9000"),
        aws_access_key_id=os.getenv("S3_ACCESS_KEY", "sticker_app"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY", "sticker_app_123"),
        config=Config(signature_version="s3v4"),
        region_name=os.getenv("S3_REGION", "us-east-1"),
    )

app = FastAPI(title=APP_NAME)

@app.get("/health")
def health():
    try:
        with get_db_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                _ = cur.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"db_unhealthy: {e}")

    try:
        s3 = get_s3_client()
        bucket = os.getenv("S3_BUCKET", "sticker-images")
        s3.head_bucket(Bucket=bucket)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"s3_unhealthy: {e}")

    return {"status": "ok", "service": APP_NAME}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    bucket = os.getenv("S3_BUCKET", "sticker-images")

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image uploads are allowed")

    key = f"uploads/{file.filename}"

    try:
        s3 = get_s3_client()
        s3.upload_fileobj(
            Fileobj=file.file,
            Bucket=bucket,
            Key=key,
            ExtraArgs={"ContentType": file.content_type},
        )
        # local dev URL (served by MinIO)
        public_url = f"http://localhost:9000/{bucket}/{key}"
        return {"bucket": bucket, "key": key, "url": public_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
