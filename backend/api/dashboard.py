from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database.database import get_db

from backend.database.models import (
    Session as SessionModel,
    RiskEvent,
    BehaviorSample
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/overview")
def get_dashboard_overview(
    db: Session = Depends(get_db)
):

    total_verifications = (
        db.query(BehaviorSample).count()
    )


    verified_sessions = db.query(SessionModel).filter(
    SessionModel.status.in_(["ACTIVE", "VERIFIED"])
).count()


    average_typing_speed = (
        db.query(
            func.avg(
                BehaviorSample.typing_speed
            )
        )
        .scalar()
    )


    active_sessions = (
        db.query(SessionModel)
        .filter(
            SessionModel.status == "ACTIVE"
        )
        .count()
    )


    return {

        "total_verifications":
            total_verifications,

        "verified_sessions":
            verified_sessions,

        "average_typing_speed":
            round(
                average_typing_speed or 0,
                2
            ),

        "active_sessions":
            active_sessions,

        "system_status":
            "ACTIVE"
    }


@router.get("/activity")
def get_recent_activity(
    db: Session = Depends(get_db)
):

    events = (
        db.query(RiskEvent)
        .order_by(
            RiskEvent.timestamp.desc()
        )
        .limit(10)
        .all()
    )


    activities = []

    for event in events:

        activities.append({

            "id": event.id,

            "session_id":
                event.session_id,

            "timestamp":
                event.timestamp,

            "risk_score":
                event.risk_score,

            "risk_level":
                event.risk_level,

            "action":
                event.action,

            "reason":
                event.reason
        })


    return {
        "activities": activities
    }