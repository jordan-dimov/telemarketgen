from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.settings import settings


engine = create_engine(settings.sqlite_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class VideoClip(Base):
    __tablename__ = "videoclips"

    id = Column(Integer, primary_key=True, index=True)
    generation_uuid = Column(String, index=True)
    generation_phase = Column(String, default="Initiated")
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    duration_seconds = Column(Integer, default=0)
    initiated_at = Column(DateTime)
    created_at = Column(DateTime, nullable=True)
    path_to_video = Column(String, nullable=True)
    generation_output = Column(String, nullable=True)

    @property
    def video_url(self):
        fn = self.path_to_video.split("/")[-1]
        return f"/clips/{self.title}/{fn}"
