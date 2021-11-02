import mimetypes
from pathlib import Path
from fastapi import HTTPException
from starlette import status
from starlette.responses import Response


def apply_cache_headers(response: Response) -> None:
    cache_params = (
        "public",
        "must-revalidate"
    )
    response.headers["Cache-Control"] = ",".join(cache_params)


def static_response(file_name: str) -> Response:
    def get_file_path_safe() -> Path:
        file_path = Path(file_name).resolve()
        if not file_path.is_file():
            raise HTTPException(
                detail=f"file {file_name!r} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return file_path

    def calc_media_type() -> str:
        return mimetypes.guess_type(file_name)[0] or "text/plain"

    file_path = get_file_path_safe()
    media_type = calc_media_type()

    with file_path.open("rb") as stream:
        content = stream.read()
        return Response(content=content, media_type=media_type)