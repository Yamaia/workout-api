from fastapi import FastAPI
from fastapi_pagination import add_pagination

from workout_api.routers import api_router

app = FastAPI(title="WorkoutAPI", description="API de competição de crossfit")
app.include_router(api_router)
add_pagination(app)
