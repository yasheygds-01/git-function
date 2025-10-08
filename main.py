import logging
import functions_framework
import argparse
import json
from datetime import datetime, timezone

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def hello_gcs(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    logging.info("=============== CODE LOG ===================")
    logging.info(f"Event ID: {event_id}")
    logging.info(f"Event type: {event_type}")
    logging.info(f"Bucket: {bucket}")
    logging.info(f"File: {name}")
    logging.info(f"Metageneration: {metageneration}")
    logging.info(f"Created: {timeCreated}")
    logging.info(f"Updated: {updated}")
    logging.info("===========================================")

if __name__ == "__main__":
    # Simple local runner to invoke hello_gcs with required args

    parser = argparse.ArgumentParser(description="Local runner for hello_gcs CloudEvent handler")
    parser.add_argument("--json", dest="json_path", help="Path to a JSON file containing CloudEvent 'id', 'type' and 'data' with GCS event fields")
    parser.add_argument("--bucket", help="GCS bucket name")
    parser.add_argument("--name", help="Object name")
    parser.add_argument("--metageneration", default="1", help="Object metageneration")
    parser.add_argument("--timeCreated", help="Creation time RFC3339 (default: now)")
    parser.add_argument("--updated", help="Updated time RFC3339 (default: now)")
    parser.add_argument("--event-id", default="0000000000000000", help="CloudEvent id")
    parser.add_argument("--event-type", default="google.cloud.storage.object.v1.finalized", help="CloudEvent type")
    parser.add_argument("--sample", action="store_true", help="Use sample data if no args provided")

    args = parser.parse_args()

    # Build a minimal CloudEvent-like object with .data and item access
    class LocalCloudEvent(dict):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.data = kwargs.get("data", {})

    def now_rfc3339():
        return datetime.now(timezone.utc).isoformat()

    if args.json_path:
        with open(args.json_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        cloud_event = LocalCloudEvent(**payload)
    else:
        if args.sample and not args.bucket and not args.name:
            bucket = "example-bucket"
            name = "path/to/file.txt"
        else:
            if not args.bucket or not args.name:
                raise SystemExit("--bucket and --name are required unless --json or --sample is used")
            bucket = args.bucket
            name = args.name

        time_created = args.timeCreated or now_rfc3339()
        updated = args.updated or time_created
        cloud_event = LocalCloudEvent(
            id=args.event_id,
            type=args.event_type,
            data={
                "bucket": bucket,
                "name": name,
                "metageneration": args.metageneration,
                "timeCreated": time_created,
                "updated": updated,
            },
        )

    hello_gcs(cloud_event)
