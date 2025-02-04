from qm9star_query.api.main import api_router
from qm9star_query.core.config import settings
from qm9star_query.core.db import engine, init_db
from fastapi import FastAPI
from fastapi.routing import APIRoute
from sqlmodel import Session
from starlette.middleware.cors import CORSMiddleware


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


with Session(engine) as session:
    init_db(session)

description = """
This is a RESTful API for querying QM9* dataset, whose original paper is 
_"[QM9star, two million DFT-computed equilibrium structures for ions and radicals with atomic information](https://www.nature.com/articles/s41597-024-03933-6)"_.
And the source code of this API is available at [qm9star_query](https://github.com/gentle1999/qm9star_query).

The API provides endpoints for querying formulas, molecules, and snapshots. You can try them out in the interactive documentation.
The API schemas are shown at the end of this page.

If this dataset helps you, please cite the following paper:
```bibtex
@article{tangQM9starTwoMillion2024a,
title = {{{QM9star}}, Two Million {{DFT-computed}} Equilibrium Structures for Ions and Radicals with Atomic Information},
author = {Tang, Miao-Jiong and Zhu, Tian-Cheng and Zhang, Shuo-Qing and Hong, Xin},
year = {2024},
month = oct,
journal = {Scientific Data},
volume = {11},
number = {1},
pages = {1158},
issn = {2052-4463},
doi = {10.1038/s41597-024-03933-6},
urldate = {2024-10-22},
langid = {english}
}
```
"""

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    description=description,
    contact={
        "name": "Miao-Jiong Tang",
        "url": "https://github.com/gentle1999",
        "email": "mj_t@zju.edu.cn",
    },
    license_info={
        "name": "MIT License",
        "identifier": "MIT",
    },
    debug=settings.DEBUG,
)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)