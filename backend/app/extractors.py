from pathlib import Path
import pandas as pd
from docx import Document as DocxDocument
from PyPDF2 import PdfReader

def extract_text_generic(path: Path) -> str:
    p = Path(path)
    s = p.suffix.lower()
    try:
        if s == ".pdf":
            try:
                reader = PdfReader(str(p))
                out = []
                for page in reader.pages:
                    out.append(page.extract_text() or "")
                return "\n".join(out)
            except Exception:
                return "[PDF stored — preview unsupported by extractor]"
        elif s == ".docx":
            doc = DocxDocument(str(p))
            return "\n".join(para.text for para in doc.paragraphs)
        elif s in [".xlsx", ".xls"]:
            dfs = pd.read_excel(str(p), sheet_name=None)
            out = []
            for name, df in dfs.items():
                out.append(f"Sheet: {name}\n{df.to_csv(index=False)}")
            return "\n".join(out)
        elif s == ".txt":
            return p.read_text(errors="ignore")
        else:
            return f"[Stored {p.name} — preview unsupported]"
    except Exception as e:
        return f"[Extraction error: {e}]"
