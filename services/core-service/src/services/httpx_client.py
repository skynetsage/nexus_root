import httpx
from typing import Any, Dict, Optional, Union


class HttpxClient:

    def __init__(
        self,
        url: str,
        method: str = "GET",
        timeout: float = 30.0,
        payload: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.url = url
        self.method = method.upper()
        self.timeout = timeout
        self.payload = payload or {}
        self.headers = headers or {}

        if "Content-Type" not in self.headers and self.method in (
            "POST",
            "PUT",
            "PATCH",
        ):
            self.headers["Content-Type"] = "application/json"

    async def execute(self) -> Union[Dict[str, Any], str]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                if self.method == "GET":
                    response = await client.get(
                        self.url, params=self.payload, headers=self.headers
                    )
                elif self.method == "POST":
                    response = await client.post(
                        self.url, json=self.payload, headers=self.headers
                    )
                elif self.method == "PUT":
                    response = await client.put(
                        self.url, json=self.payload, headers=self.headers
                    )
                elif self.method == "DELETE":
                    response = await client.delete(self.url, headers=self.headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {self.method}")

                response.raise_for_status()
                try:
                    return response.json()
                except ValueError:
                    return response.text

        except httpx.RequestError as e:
            raise RuntimeError(f"Request failed: {str(e)}") from e
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
            ) from e
