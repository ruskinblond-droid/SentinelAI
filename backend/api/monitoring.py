from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database.database import get_db
from backend.database.models import (
    Session as SessionModel,
    RiskEvent,
    BehaviorSample
)

from backend.services.ml import predict
from backend.services.risk_engine import calculate_risk


router = APIRouter(
    prefix="/verification",
    tags=["Verification"]
)


# -----------------------------
# START VERIFICATION
# -----------------------------

class StartVerificationRequest(BaseModel):
    user_id: int
    device_id: int | None = None


@router.post("/start")
def start_verification(
    data: StartVerificationRequest,
    db: Session = Depends(get_db)
):

    new_session = SessionModel(
        user_id=data.user_id,
        device_id=data.device_id,
        status="ACTIVE"
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {
        "message": "Verification session started",
        "session_id": new_session.id,
        "user_id": new_session.user_id,
        "status": new_session.status
    }


# -----------------------------
# BEHAVIORAL FEATURES
# -----------------------------

class BehavioralFeatures(BaseModel):

    typing_speed: float

    mean_hold_time: float
    std_hold_time: float

    mean_flight_time: float
    std_flight_time: float

    backspace_rate: float
    pause_mean: float

    mouse_velocity_mean: float
    click_interval_mean: float


class FeatureRequest(BaseModel):

    session_id: int

    features: BehavioralFeatures


@router.post("/features")
def process_features(
    data: FeatureRequest,
    db: Session = Depends(get_db)
):

    # -----------------------------
    # 1. Find session
    # -----------------------------

    session = (
        db.query(SessionModel)
        .filter(
            SessionModel.id == data.session_id
        )
        .first()
    )

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Verification session not found"
        )


    # -----------------------------
    # 2. Check session status
    # -----------------------------

    if session.status != "ACTIVE":

        raise HTTPException(
            status_code=400,
            detail="Verification session is not active"
        )


    # -----------------------------
    # 3. Convert features
    # -----------------------------

    features = data.features.model_dump()


    # -----------------------------
    # 4. Send to ML model
    # -----------------------------

    prediction = predict(features)


    # -----------------------------
    # 5. Calculate risk
    # -----------------------------

    risk = calculate_risk(
        prediction["anomaly_score"]
    )


    # -----------------------------
    # 6. Store behavioral sample
    # -----------------------------

    sample = BehaviorSample(

        session_id=data.session_id,

        typing_speed=features["typing_speed"],

        mean_hold_time=features["mean_hold_time"],
        std_hold_time=features["std_hold_time"],

        mean_flight_time=features["mean_flight_time"],
        std_flight_time=features["std_flight_time"],

        backspace_rate=features["backspace_rate"],
        pause_mean=features["pause_mean"],

        mouse_velocity_mean=features[
            "mouse_velocity_mean"
        ],

        click_interval_mean=features[
            "click_interval_mean"
        ],

        risk_score=risk["risk_score"],
        risk_level=risk["risk_level"]
    )

    db.add(sample)


    # -----------------------------
    # 7. Store security event
    # -----------------------------

    risk_event = RiskEvent(

        session_id=data.session_id,

        risk_score=risk["risk_score"],

        risk_level=risk["risk_level"],

        action=risk["action"],

        reason="Behavioral analysis"
    )

    db.add(risk_event)

    db.commit()

    db.refresh(sample)
    db.refresh(risk_event)


    # -----------------------------
    # 8. Return result
    # -----------------------------

    return {

        "session_id": data.session_id,

        "sample_id": sample.id,

        "risk_score": risk["risk_score"],

        "risk_level": risk["risk_level"],

        "action": risk["action"],

        "confidence": prediction["confidence"],

        "timestamp": sample.timestamp
    }

@router.get("/{session_id}/status")
def get_session_status(
    session_id: int,
    db: Session = Depends(get_db)
):

    session = (
        db.query(SessionModel)
        .filter(
            SessionModel.id == session_id
        )
        .first()
    )

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )


    latest_event = (
        db.query(RiskEvent)
        .filter(
            RiskEvent.session_id == session_id
        )
        .order_by(
            RiskEvent.timestamp.desc()
        )
        .first()
    )


    if latest_event:

        return {
            "session_id": session.id,
            "status": session.status,
            "risk_score": latest_event.risk_score,
            "risk_level": latest_event.risk_level,
            "action": latest_event.action
        }


    return {
        "session_id": session.id,
        "status": session.status,
        "risk_score": 0,
        "risk_level": "UNKNOWN",
        "action": "WAITING_FOR_DATA"
    }


@router.post("/{session_id}/end")
def end_session(
    session_id: int,
    db: Session = Depends(get_db)
):

    session = (
        db.query(SessionModel)
        .filter(
            SessionModel.id == session_id
        )
        .first()
    )

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )


    session.status = "ENDED"
    session.ended_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Verification session ended",
        "session_id": session_id,
        "status": session.status
    }