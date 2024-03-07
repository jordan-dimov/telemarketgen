from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from api.models import Base, VideoClip, engine, SessionLocal

app = FastAPI()

templates = Jinja2Templates(directory="api/templates")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def list_videos(request: Request, db: Session = Depends(get_db)):
    clips = db.query(VideoClip).all()
    return templates.TemplateResponse("index.html", {"request": request, "clips": clips})
