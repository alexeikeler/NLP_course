from urllib import request
from typing import Any

class GutenbergScraper:

    @staticmethod
    def pull_text(url: str) -> str | None:

        try:
            response: Any = request.urlopen(url)
            decoded_raw_text: str = response.read().decode('utf-8')
            return decoded_raw_text.lower()

        except Exception as e:
            print(
                f'Error occurred while extracting text from url:\n{url}\n{repr(e)}'
            )
