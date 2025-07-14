import sys
import pdfplumber
import json
import glob
from typing import Dict, List

def extract_metadata(pdf_path: str) -> Dict[str, str]:
    metadata: Dict[str, str] = {}
    search_terms: Dict[str, str] = {
        "MS number:": "MS number",
        "GA Number:": "GA Number",
        "Contents:": "Contents",
        "Date:": "Date",
        "Material:": "Material",
        "Columns:": "Columns",
        "Lines per Page:": "Lines per Page",
        "Shelf Number:": "Shelf Number",
        "Dimensions:": "Dimensions",
    }

    notes: List[str] = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text: List[str] = page.extract_text().splitlines() 

                if page_text:  
                    for line in page_text:
                        if line == "Kurzgefasste Liste description:" or line == "Corrections to K–Liste description:":
                            continue

                        for search_term, key in search_terms.items():
                            if search_term in line:
                                metadata[key] = line.split(search_term, 1)[1].strip()
                                break
                        else:
                            notes.append(line)

    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}
    
    metadata["Notes"] = "\n".join(notes)
    return metadata

def dump_data(data: Dict[str, str]) -> None:
    with open('data.json', 'w') as output_file:
        json.dump(data, output_file)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        pdf_files = glob.glob("*.pdf")  
        for pdf_file in pdf_files:
            metadata = extract_metadata(pdf_file)
            dump_data(metadata)
            if metadata:
                print(f"Processed {pdf_file}:")
                for key, value in metadata.items():
                    print(f"{key}: {value}")
            else:
                print(f"No matching lines found in {pdf_file}.")   

    elif len(sys.argv) == 2:
        pdf_file = sys.argv[1]
        metadata = extract_metadata(pdf_file)
        dump_data(metadata)
        if metadata:
            for key, value in metadata.items():
                print(f"{key}: {value}") 
        else:
            print("No matching lines found in the PDF.")   

    else:
        print("Usage: python curator.py <path_to_pdf> or run without arguments.")

