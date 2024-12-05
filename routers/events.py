from fastapi import routing, Depends
from midnite.models.validation.event import EventPayload, EventResponse
from midnite.methods.code_handler import FraudDetection, get_fraud_detection

router = routing.APIRouter()


@router.post("/event")
def read_event(
    payload: EventPayload, fd: FraudDetection = Depends(get_fraud_detection)
) -> EventResponse:
    """
    Event endpoint that handles the fraud detection for withdraws and deposits
    """
    codes = fd.run_fraud_detection(
        payload.amount,
        str(payload.user_id),
        transaction_type=str(payload.type_),
        second_received=int(payload.t),
    )
    code_list = [c.value for c in codes if c is not None]
    alert_flag = True if codes else False
    return EventResponse(
        alert=alert_flag,
        alert_codes=code_list,
        user_id=payload.user_id,
    )
