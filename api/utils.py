from starlette.requests import Request

from api.models import SessionLocal


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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
