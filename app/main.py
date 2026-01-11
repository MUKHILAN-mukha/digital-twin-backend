from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine

from app.routers import auth, student, parent
from app.routers import student_profile
from app.routers import student_events
from app.routers import digital_twin
from app.routers import admin
from app.routers import ml
from app.routers import analytics
from app.routers import insights
from app.routers import recommendations
from app.routers import dashboard
from app.routers import insight_reviews
from app.routers import admin_dashboard




app = FastAPI(title="Digital Twin Backend")

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(parent.router)
app.include_router(student_profile.router)
app.include_router(student_events.router)
app.include_router(digital_twin.router)
app.include_router(admin.router)
app.include_router(ml.router)
app.include_router(analytics.router)
app.include_router(insights.router)
app.include_router(recommendations.router)
app.include_router(dashboard.router)
app.include_router(insight_reviews.router)
app.include_router(admin_dashboard.router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
