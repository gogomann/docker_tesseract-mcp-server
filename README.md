# Tesseract PDF MCP Server

A Model Context Protocol (MCP) server that provides OCR capabilities for PDF documents using Tesseract OCR. This server allows AI assistants to extract text from PDF files, supporting multiple languages including English and Simplified Chinese out of the box.

## Features

- **PDF to Text Conversion**: Extract text from PDF documents using OCR technology
- **Multi-language Support**: Process documents in multiple languages (English and Simplified Chinese by default)
- **Dockerized Solution**: Easy deployment with Docker
- **MCP Integration**: Seamlessly integrates with AI assistants that support the Model Context Protocol

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your system

## Build Instructions

Build the Docker image with the following command:

```bash
docker build -t tesseract-pdf-mcp .
```

## Running the Server

Run the MCP server with the following command:

```bash
docker run -it --rm \
  -v /path/to/your/pdfs:/pdfs \
  tesseract-pdf-mcp
```

### Important Notes:

- The `-v /path/to/your/pdfs:/pdfs` option mounts a volume from your host system to the Docker container, allowing the server to access PDF files.
- Replace `/path/to/your/pdfs` with the actual path to the directory containing your PDF files.
- The server will be accessible via standard input/output (stdio) as specified in the MCP protocol.

## Usage

The server provides a tool called `convert_pdf` that can be used to extract text from PDF files.

### Input

The `convert_pdf` tool accepts the following JSON input:

```json
{
  "file_path": "/pdfs/document.pdf",
  "language": "eng"
}
```

Parameters:
- `file_path` (required): Path to the PDF file to process. This should be the path inside the container (e.g., `/pdfs/document.pdf`).
- `language` (optional): Language for OCR processing. Default is `"eng"` (English).
  - Available languages by default: `"eng"` (English), `"chi_sim"` (Simplified Chinese)

### Output

The tool returns a JSON response with the following structure:

```json
{
  "status": "success",
  "output_path": "/pdfs/document.txt"
}
```

On success:
- `status`: Will be `"success"`
- `output_path`: The absolute path to the generated text file

On error:
- `status`: Will be `"error"`
- `message`: Error description
- `output_path`: Will be `null`

### Example Usage

When connected to an AI assistant that supports MCP:

1. The assistant can use the `convert_pdf` tool to extract text from a PDF file
2. The text file will be created in the same directory as the PDF file
3. The assistant can then access the text file to analyze its contents

## Connecting to AI Tools

To connect this MCP server to AI tools that support the Model Context Protocol, you'll need to configure the tool with the appropriate settings.

### Configuration Example

Add the following configuration to your AI tool's settings:

```json
{
  "mcpServers": {
    "tesseract-pdf-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "/path/to/your/pdfs:/pdfs",
        "tesseract-pdf-mcp"
      ],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Make sure to replace `/path/to/your/pdfs` with the actual path to your PDF files directory.

### Usage with AI Tools

Once connected:
1. The AI tool will have access to the `convert_pdf` tool provided by this MCP server
2. You can ask the AI to extract text from PDF documents
3. The AI will use the MCP server to process the PDFs and access the resulting text

## Adding More Languages

The server comes with English (`eng`) and Simplified Chinese (`chi_sim`) language support by default. To add more languages:

1. Modify the `Dockerfile` by adding additional language packs to the `apt-get install` command:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-chi-sim \
    tesseract-ocr-fra \    # Add French
    tesseract-ocr-deu \    # Add German
    tesseract-ocr-spa \    # Add Spanish
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

2. Rebuild the Docker image:

```bash
docker build -t tesseract-pdf-mcp .
```

### Available Language Codes

Some common language codes for Tesseract OCR:

- `eng`: English
- `chi_sim`: Simplified Chinese
- `chi_tra`: Traditional Chinese
- `fra`: French
- `deu`: German
- `spa`: Spanish
- `ita`: Italian
- `jpn`: Japanese
- `kor`: Korean
- `rus`: Russian

For a complete list of available language packs, refer to the [Tesseract documentation](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html).

## Debugging Inside the Container

If you need to debug or test the PDF conversion logic directly inside the container, follow these steps:

### Starting an Interactive Shell

Launch an interactive shell session in the container with the following command:

```bash
docker run --rm -it -v /path/to/your/pdfs:/data tesseract-pdf-mcp /bin/bash
```

This command:
- Creates a container from the `tesseract-pdf-mcp` image
- Mounts your local PDF directory to `/data` inside the container
- Overrides the default command to start a bash shell
- Removes the container automatically when you exit (`--rm`)

### Working Inside the Container

Once inside the container's shell, you can:
- Navigate the filesystem using standard Linux commands (`cd`, `ls`, etc.)
- Access your mounted PDFs in the `/data` directory
- Run Python scripts or start an interactive Python session

### Testing the Conversion Function

You can test the PDF to text conversion directly using Python's interactive shell:

```bash
# Start Python interactive shell
python3
```

```python
# Import the conversion function
from ocr.converter import pdf_to_text

# Process a PDF file (replace with your actual filename)
output_path = pdf_to_text('/data/my_document.pdf', lang='eng')

# Verify the result
print(f"Conversion successful. Output saved to: {output_path}")

# Exit Python shell
exit()
```

The converted text file will be saved in the same directory as your PDF file (in the `/data` directory), making it accessible from your host machine as well.