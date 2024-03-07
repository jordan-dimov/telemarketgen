import uuid

from fastapi import FastAPI, Depends, Request, Form, BackgroundTasks
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from api.background_tasks import create_video_clip
from api.settings import settings
from api.models import Base, VideoClip, engine
from api.utils import flash, get_flashed_messages, get_db

app = FastAPI(
    title=settings.app_name,
    middleware=[Middleware(SessionMiddleware, secret_key=settings.session_secret)],
)

templates = Jinja2Templates(directory="api/templates")
templates.env.globals["get_flashed_messages"] = get_flashed_messages

Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
def list_videos(request: Request, db: Session = Depends(get_db)):
    clips = db.query(VideoClip).all()
    return templates.TemplateResponse(
        "index.html", {"request": request, "clips": clips}
    )


@app.post("/new-clip/")
def new_clip(
    request: Request,
    background_tasks: BackgroundTasks,
    title: str = Form(None),
    db: Session = Depends(get_db),
):
    generation_id = str(uuid.uuid4())
    title = title or "Untitled"
    description = "No description"
    background_tasks.add_task(create_video_clip, db, generation_id, title, description)
    flash(request, f"A new video is being generated: {generation_id}", "success")
    # Redirect to the home page
    return RedirectResponse("/", status_code=303)


@app.get("/clip/{clip_id}/")
def show_clip(clip_id: int, request: Request, db: Session = Depends(get_db)):
    clip = db.query(VideoClip).filter(VideoClip.id == clip_id).first()
    return templates.TemplateResponse("clip.html", {"request": request, "clip": clip})
