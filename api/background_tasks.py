from pathlib import Path
from sqlalchemy.orm import Session
from datetime import datetime

from ai.audio import generate_speech, generate_music, get_wav_duration
from ai.images import generate_image
from ai.video import generate_telemarketing_video
from api.models import VideoClip
from api.settings import settings


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

    output_folder = Path(settings.output_folder) / generation_uuid
    output_folder.mkdir(parents=True, exist_ok=True)

    db.path_to_video = str(output_folder / "telemarketing.mp4")

    image_paths = []
    for n in range(1, 4):
        db_video.generation_phase = f"Images: {n} of 3"
        db.commit()
        db.refresh(db_video)
        img_path = str(output_folder / f"product{n}.jpg")
        generate_image(db_video.title, img_path)
        image_paths.append(img_path)

    db_video.generation_phase = "Speech"
    db.commit()
    db.refresh(db_video)
    generate_speech(description, str(output_folder / "speech.wav"))

    db_video.generation_phase = "Music"
    db.commit()
    db.refresh(db_video)
    generate_music(
        "Telemarketing-style background music to advertise a novel, modern consumer product",
        30,
        str(output_folder / "music.wav"),
    )

    total_length = get_wav_duration(str(output_folder / "speech.wav")) + 1

    db_video.duration_seconds = total_length
    db_video.generation_phase = "Video"
    db.commit()
    db.refresh(db_video)
    generate_telemarketing_video(
        image_paths,
        str(output_folder / "music.wav"),
        str(output_folder / "speech.wav"),
        total_length,
        db_video.path_to_video,
    )

    db_video.generation_phase = "Completed"
    db_video.created_at = datetime.now()
    db.commit()
    db.refresh(db_video)

    return db_video
