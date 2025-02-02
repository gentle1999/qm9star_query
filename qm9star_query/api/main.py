'''
Author: TMJ
Date: 2025-02-02 16:35:58
LastEditors: TMJ
LastEditTime: 2025-02-02 16:59:48
Description: 请填写简介
'''
from fastapi import APIRouter

from qm9star_query.api.routes import formula, molecules, snapshots, utils

api_router = APIRouter()
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(formula.router, prefix="/formulas", tags=["formulas"])
api_router.include_router(molecules.router, prefix="/molecules", tags=["molecules"])
api_router.include_router(snapshots.router, prefix="/snapshots", tags=["snapshots"])
