import uuid

from fastapi import FastAPI, Depends, Request, Form, BackgroundTasks
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from api.settings import settings
from api.models import Base, VideoClip, engine, SessionLocal

app = FastAPI(
    title=settings.app_name,
    middleware=[Middleware(SessionMiddleware, secret_key=settings.session_secret)],
)

templates = Jinja2Templates(directory="api/templates")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def flash(request: Request, message: str, category: str = "") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append({"message": message, "category": category})


def get_flashed_messages(request: Request):
    if "_messages" not in request.session:
        return []
    messages = request.session["_messages"]
    del request.session["_messages"]
    return messages


def create_video_clip(db: Session, generation_uuid: str, title: str, description: str):
    db_video = VideoClip(
        generation_uuid=generation_uuid,
        generation_phase="Initiated",
        title=title,
        description=description,
        duration_seconds=0,
        path_to_video="",
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


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
