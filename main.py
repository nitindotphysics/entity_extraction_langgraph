import warnings
warnings.filterwarnings("ignore")

from app.ingestion.file_discovery import (
    discover_pdfs
)

from app.graph.workflow import (
    graph
)


def main():

    pdfs = discover_pdfs()

    for pdf in pdfs:

        print("\n" + "=" * 80)
        print(f"PROCESSING: {pdf['file_name']}")
        print("=" * 80)

        initial_state = {

            "skip_processing": False,

            "file_path": pdf["file_path"],

            "representation": None,

            "quality_report": None,

            "classification": None,

            "extracted_entities": None,

            "normalized_entities": None,

            "requires_ocr": None,

            "alerts": [],

            "document_id": None,

            "workflow_run_id": None,

            "execution_order": 0
        }

        result = graph.invoke(
            initial_state
        )

        print("\nFINAL GRAPH STATE:\n")

        print(result)


if __name__ == "__main__":

    main()