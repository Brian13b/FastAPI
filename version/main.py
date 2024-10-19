import json
import pathlib
from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from fastapi.middleware.cors import CORSMiddleware  

# configure logging
logconfig_file = pathlib.Path('logconfig.json')
if logconfig_file.exists():
    with open(logconfig_file) as jsonfile:
        logconfig_dict = json.load(jsonfile)
        dictConfig(logconfig_dict)

from api.controllers.contactos_api import contactos_router
from api.controllers.localidades_api import localidades_router
from api.controllers.provincias_api import provincias_router
from data.database import connect_to_prod

connect_to_prod()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Cambia esto a tu origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def show_docs():
    return RedirectResponse(url="/docs")


app.include_router(contactos_router)
app.include_router(localidades_router)
app.include_router(provincias_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
