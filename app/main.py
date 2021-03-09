# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0

import sys

sys.path.insert(0, "/")
from typing import List, Dict

from fastapi import FastAPI
from os2mo_http_trigger_protocol import (
    EventType,
    MOTriggerPayload,
    MOTriggerRegister,
    RequestType,
)
from structlog import get_logger

from app.config import get_settings
from app.tracing import setup_instrumentation, setup_logging

app = FastAPI()


@app.get(
    "/triggers",
    tags=["Trigger API"],
    summary="List triggers to be registered.",
    response_model=List[MOTriggerRegister],
    response_description=(
        "Successful Response" + "<br/>" + "List of triggers to register."
    ),
)
def triggers():
    """List triggers to be registered."""
    return [
        {
            "event_type": EventType.ON_BEFORE,
            "request_type": RequestType.EDIT,
            "role_type": "org_unit",
            "url": "/triggers/ou/edit",
        }
    ]


@app.post(
    "/triggers/ou/edit",
    tags=["Trigger API"],
    summary="Log that an organizational unit and print settings value",
    response_model=Dict[str, str],
)
async def triggers_ou_edit(payload: MOTriggerPayload):
    """Fired when an OU has been created."""
    logger = get_logger()
    logger.info("triggers_ou_edit", payload=payload.json())
    return {"configured_value": get_settings().configured_value}


app = setup_instrumentation(app)
setup_logging()
