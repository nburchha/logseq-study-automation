---
name: read-pdf
description: Parses text and document structure from a local PDF file to enable programmatic reading of lecture slides or readings.
---
# Skill: read-pdf

## Schema
### Inputs
```json
{
  "type": "object",
  "properties": {
    "pdf_path": {
      "type": "string",
      "description": "The absolute or relative path to the local PDF file."
    },
    "pages": {
      "type": "string",
      "description": "Optional page range to extract (e.g., '1-5', '10,12,15'). Defaults to all pages."
    }
  },
  "required": ["pdf_path"]
}
```

### Outputs
```json
{
  "type": "object",
  "properties": {
    "text": {
      "type": "string",
      "description": "The extracted raw text content from the PDF."
    },
    "structure": {
      "type": "object",
      "description": "The document outline, headers, and metadata (if available)."
    },
    "error": {
      "type": "string",
      "description": "Error message if parsing fails."
    }
  }
}
```

## Logic
1. Validate that the file exists at `pdf_path` and has a `.pdf` extension.
2. Utilize a robust PDF parsing library (e.g., `pdfminer.six` or `PyPDF2` in Python, or `pdf2json` in Node.js).
3. Extract textual content, optionally restricted by the `pages` parameter.
4. Attempt to extract the document outline (TOC) to populate the `structure` object.
5. Return the parsed text and structural metadata.
