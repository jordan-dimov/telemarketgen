from sqlalchemy.orm import Session
from datetime import datetime
from api.models import VideoClip


def create_video_clip(db: Session, generation_uuid: str, title: str, description: str):
    db_video = VideoClip(
        generation_uuid=generation_uuid,
        generation_phase="Initiated",
        title=title,
        description=description,
        duration_seconds=0,
        path_to_video="",
        initiated_at=datetime.now(),
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video
