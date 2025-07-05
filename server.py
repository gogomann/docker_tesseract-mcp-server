from typing import Dict, Any
import os
from mcp.server.fastmcp import FastMCP
from ocr.converter import pdf_to_text

# Initialize the MCP server
mcp = FastMCP("tesseract-pdf-mcp")

@mcp.tool()
async def convert_pdf(file_path: str, language: str = "eng") -> Dict[str, Any]:
    """
    Convert a PDF file to text using OCR.
    
    Args:
        file_path (str): Path to the PDF file to process
        language (str): Language for OCR (e.g., 'eng', 'chi_sim')
        
    Returns:
        Dict[str, Any]: A dictionary containing the status and output path
    """
    try:
        output_path = pdf_to_text(file_path, language)
        return {
            "status": "success",
            "output_path": os.path.abspath(output_path)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "output_path": None
        }

if __name__ == "__main__":
    mcp.run(transport='stdio')
