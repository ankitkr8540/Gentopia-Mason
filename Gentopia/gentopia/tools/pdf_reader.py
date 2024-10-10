from typing import AnyStr, Optional, Type, Any
from PyPDF2 import PdfReader
from gentopia.tools.basetool import *


class PdfReaderArgs(BaseModel):
    path_to_pdf: str = Field(..., description="path to the pdf file.")


class PdfTextExtractor(BaseTool):
    name = "pdf_reader"
    description = "Extracting text from a pdf file, the output is the extracted text."
    args_schema: Optional[Type[BaseModel]] = PdfReaderArgs

    def _run(self, path_to_pdf: AnyStr) -> AnyStr:
        with open(path_to_pdf, "rb") as f:
            pdf = PdfReader(f)
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = PdfTextExtractor()._run("Attention for transformer.pdf")
    print(ans)