from fastapi import routing
from midnite.models.validation.event import EventPayload, EventResponse
from midnite.methods.code_handler import FraudDetection

fd = FraudDetection()
router = routing.APIRouter()


@router.post("/event")
def read_event(payload: EventPayload) -> EventResponse:
    """
    Event endpoint that handles the fraud detection for withdraws and deposits
    """
    codes = fd.run_fraud_detection(
        payload.amount,
        payload.user_id,
        transaction_type=payload.type_,
        second_received=payload.t,
    )
    codes = [c.value for c in codes if c is not None]
    alert_flag = True if codes else False
    return EventResponse(
        alert=alert_flag,
        alert_codes=codes,
        user_id=payload.user_id,
    )
