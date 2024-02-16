from magic import from_buffer
from mimetypes import guess_extension
from src.planner.users.domain.mime_guesser import MimeGuesser
from kink import inject

@inject(use_factory=True, alias=MimeGuesser)
class MagicMimeGuesser:
    def extension(self, file: bytes) -> str:
        content_type = from_buffer(file, mime=True)
        return guess_extension(content_type)
