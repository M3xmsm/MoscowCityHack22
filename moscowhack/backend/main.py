from typing import Dict, List, Any

from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware

from moscowhack.backend.postgres import (
    get_postgres_connection,
    CompaniesInfo,
    MoscowProducts,
    AnalyticsDataTry,
)

pg_client = get_postgres_connection()
pg_client.bind([CompaniesInfo, MoscowProducts])

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/company/get/{inn}")
async def get_company_by_inn(
        inn: str = Path(None, min_length=10, max_length=12, regex="^[0-9]+$")
) -> Dict[str, Any]:
    with pg_client:
        if inn is not None:
            result = CompaniesInfo.select().where(CompaniesInfo.inn == inn)
            return list(result.dicts())[0]
        else:
            return {}


@app.get("/product/get/{inn}")
async def get_products_by_inn(
        inn: str = Path(None, min_length=10, max_length=12, regex="^[0-9]+$")
) -> List[Dict[str, Any]]:
    with pg_client:
        if inn is not None:
            result = MoscowProducts.select().where(MoscowProducts.inn == inn)
            return list(result.dicts())
        else:
            return []


@app.get("/analytics/get/{inn}")
async def get_analytics_by_inn(
        inn: str = Path(None, min_length=10, max_length=12, regex="^[0-9]+$")
) -> Dict[str, Any]:
    with pg_client:
        if inn is not None:
            result = AnalyticsDataTry.select().where(AnalyticsDataTry.inn == inn)
            return result.dicts()[0]
        else:
            return {}