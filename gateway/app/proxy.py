import httpx
from fastapi import HTTPException, Request, Response, status

client = httpx.AsyncClient(timeout=10)

_REQUEST_HEADERS = {"accept", "authorization", "content-type", "cookie"}
_SKIP_RESPONSE_HEADERS = {
    "connection",
    "content-encoding",
    "content-length",
    "date",
    "server",
    "transfer-encoding",
}


async def forward(request: Request, upstream: str) -> Response:
    path = request.scope["path"]
    segments = path.split("/")
    if not path.startswith("/") or any(s in (".", "..") or "\\" in s for s in segments):
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    try:
        url = httpx.URL(upstream).copy_with(
            path=path,
            query=request.scope["query_string"] or None,
        )
    except httpx.InvalidURL:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    try:
        upstream_response = await client.request(
            request.method,
            url,
            headers={k: v for k, v in request.headers.items() if k in _REQUEST_HEADERS},
            content=await request.body(),
        )
    except httpx.TimeoutException:
        raise HTTPException(status.HTTP_504_GATEWAY_TIMEOUT, "upstream timeout")
    except httpx.TransportError:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "upstream unavailable")

    response = Response(upstream_response.content, upstream_response.status_code)
    for key, value in upstream_response.headers.multi_items():
        if key not in _SKIP_RESPONSE_HEADERS:
            response.headers.append(key, value)
    return response
