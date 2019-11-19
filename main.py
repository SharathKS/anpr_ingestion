"""Cloud function to save ANPR data

Camera sends data to this function which saves a raw copy
of the data and also separates out the metadata, number plate
image (plate) and vehicle image (overview).

Deploy the cloud function

    gcloud beta functions \
        deploy anpr_ingestion \
        --runtime python37 \
        --trigger-http \
        --project nexus-cf-test

Use the following URL to send camera data to this function substituting
as follows;

    {region}    Region (eg "europe-west2")
    {project}   GCP project id (eg "nexus-ingress-dev").
    {deviceId}  Camera id
    {token}     Token

    https://{region}-{project}.cloudfunctions.net?deviceId={device-id}&token={token}
"""

import json
from google.cloud import firestore
from google.cloud import logging
from get_vehicle_data import get_vehicle_data

# ---- log name
LOGNAME = "anpr_ingestion"


def create_log(logname):
    # ------------------
    """Create logging object

    return  -- logging object
    logname -- log name
    """
    log_client = logging.Client()
    return log_client.logger(logname)


# ---- create the logger
LOG = create_log(LOGNAME)

# ---- create a firestore database object
DB = firestore.Client()

VALID_ARGS = ["deviceId", "token"]

def anpr_ingestion(request):
    # ----------------------
    """Read ANPR capture data from camera

    Camera sends a POST request with the following query parameters.
        deviceId
        token
    """
    global VALID_ARGS

    try:
        response = {"status": "ok"}
        status_code = 200
        request_json = request.get_json()

        LOG.log_text("anpr_ingestion args: {}, json: {}".format(request.args, request_json))

        device_id = request.args.get("deviceId", None)
        token = request.args.get("token", None)

        if not device_id or not token:
            LOG.log_text("invalid or missing query parameter(s)", severity="ERROR")
            status_code = 401
            response["msg"] = "invalid query parameter(s)"
            return json.dumps(response), status_code

        request_json = request.get_json()

        # ---- get vrm from request
        vrm = request_json["decodes"][0]["vrm"]

        # ---- get vehicle details
        doc_id, vehicle = get_vehicle_data(DB, vrm)
        response["doc_id"] = doc_id
        response["vehicle"] = vehicle


    except Exception as exc:
        # ---- catch any unhandled exceptions
        status_code = 500
        response = {"status": "fail",
                    "msg": str(exc)}
        LOG.log_text("caught exception: {}".format(response), severity="ERROR")

    return json.dumps(response), status_code
