from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine
from gemini_service import generate_plan

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder
templates = Jinja2Templates(directory="templates")


# Home page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# Generate fitness plan
@app.post("/generate", response_class=HTMLResponse)
def generate(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    weight: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    db: Session = SessionLocal()

    try:

        # Generate AI plan
        plan = generate_plan(age, weight, goal, intensity)

        # Save to database
        user_plan = models.UserPlan(
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
            plan=plan
        )

        db.add(user_plan)
        db.commit()

    finally:
        db.close()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "plan": plan
        }
    )