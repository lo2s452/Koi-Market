from fastapi import APIRouter, Depends, Request, Response

from app.config import settings
from app.deps import require_access_token
from app.proxy import forward

router = APIRouter()

ANY = ["GET", "POST", "PATCH", "DELETE"]


def _route(path: str, methods: list[str], upstream: str, *, protected: bool) -> None:
    async def endpoint(request: Request) -> Response:
        return await forward(request, upstream)

    dependencies = [Depends(require_access_token)] if protected else []
    router.add_api_route(path, endpoint, methods=methods, dependencies=dependencies)


_route("/auth/register", ["POST"], settings.auth_url, protected=False)
_route("/auth/login", ["POST"], settings.auth_url, protected=False)
_route("/auth/refresh", ["POST"], settings.auth_url, protected=False)
_route("/auth/logout", ["POST"], settings.auth_url, protected=False)
_route("/products", ["GET"], settings.core_url, protected=False)
_route("/products/{product_id}", ["GET"], settings.core_url, protected=False)
_route("/static/{path:path}", ["GET"], settings.core_url, protected=False)

_route("/auth/admin/{path:path}", ANY, settings.auth_url, protected=True)
_route("/me", ["GET"], settings.core_url, protected=True)
_route("/cart", ANY, settings.core_url, protected=True)
_route("/cart/{path:path}", ANY, settings.core_url, protected=True)
_route("/orders", ANY, settings.core_url, protected=True)
_route("/orders/{path:path}", ANY, settings.core_url, protected=True)
_route("/admin/{path:path}", ANY, settings.core_url, protected=True)
