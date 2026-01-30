#!/bin/sh
set -e

echo "⏳ Waiting for MinIO..."
until mc alias set local http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD" >/dev/null 2>&1; do
  sleep 2
done
echo "✅ MinIO is ready"

echo "📦 Creating bucket: $MINIO_BUCKET_NAME"
mc mb --ignore-existing "local/$MINIO_BUCKET_NAME" >/dev/null

echo "📜 Creating policy: sticker-policy"
mc admin policy create local sticker-policy /policies/sticker-policy.json >/dev/null 2>&1 || true

echo "👤 Creating app user: $MINIO_APP_USER"
mc admin user add local "$MINIO_APP_USER" "$MINIO_APP_PASSWORD" >/dev/null 2>&1 || true

echo "🔐 Attaching policy to user"
mc admin policy attach local sticker-policy --user "$MINIO_APP_USER" >/dev/null

echo "🎉 MinIO initialization completed"
