import os
import boto3
from pathlib import Path
from utils import clean_text
import json

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

def extract_from_image(client, image_bytes):
    # Use Textract detect_document_text for handwritten + printed text
    # For handwriting, ANALYZE_DOCUMENT can be used with feature types, but detect_document_text works for many cases
    resp = client.detect_document_text(Document={'Bytes': image_bytes})
    # resp['Blocks'] contains lines and words
    lines = []
    for block in resp.get("Blocks", []):
        if block.get("BlockType") == "LINE":
            lines.append(block.get("Text", ""))
    return "\n".join(lines)

def process_files(input_dir: str, output_json: str):
    textract = boto3.client("textract", region_name=AWS_REGION)
    results = []
    p = Path(input_dir)
    for file in p.iterdir():
        if not file.is_file():
            continue
        ext = file.suffix.lower()
        if ext in [".png", ".jpg", ".jpeg", ".tiff", ".pdf"]:
            print("Processing", file.name)
            with open(file, "rb") as f:
                image_bytes = f.read()
            text = extract_from_image(textract, image_bytes)
            cleaned = clean_text(text)
            results.append({
                "file": str(file),
                "text": cleaned
            })
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Saved extracted text to", output_json)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="sample_data", help="Input folder with images/PDFs")
    parser.add_argument("--output", default="models/extracted.json", help="Output JSON with extracted text")
    args = parser.parse_args()
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    process_files(args.input, args.output)
