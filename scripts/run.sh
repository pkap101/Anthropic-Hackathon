#!/bin/bash
echo "🦄 Starting uvicorn"

echo "/usr/local/bin/uvicorn src.app:app --workers 1  --host 0.0.0.0  --port 8080 --access-log"
/usr/local/bin/uvicorn src.app:app --workers 1  --host 0.0.0.0  --port 8080 --access-log
