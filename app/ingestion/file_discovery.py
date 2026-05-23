from pathlib import Path
from datetime import datetime


INPUT_FOLDER = Path("data/input")


def discover_pdfs():

    pdf_files = list(INPUT_FOLDER.glob("*.pdf"))

    discovered_files = []

    for pdf in pdf_files:

        file_info = {
            "file_name": pdf.name,
            "file_path": str(pdf),
            "file_size_kb": round(pdf.stat().st_size / 1024, 2),
            "created_time": datetime.fromtimestamp(
                pdf.stat().st_ctime
            ).strftime("%Y-%m-%d %H:%M:%S")
        }

        discovered_files.append(file_info)

    return discovered_files