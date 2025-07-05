import os
import pytesseract
from pdf2image import convert_from_path
from tqdm import tqdm

def pdf_to_text(file_path: str, lang: str = "eng") -> str:
    """
    Performs OCR on a PDF file and saves the extracted text.
    
    Args:
        file_path (str): Path to the PDF file to process
        lang (str): Language for OCR (e.g., 'eng', 'chi_sim')
        
    Returns:
        str: Path to the output text file
    """
    # Validate input
    if not os.path.isfile(file_path) or not file_path.lower().endswith('.pdf'):
        raise ValueError(f"Error: The path {file_path} is not a valid PDF file.")
    
    try:
        # Get the directory and filename without extension
        input_dir = os.path.dirname(file_path)
        pdf_filename = os.path.splitext(os.path.basename(file_path))[0]
        
        # Output file will be in the same directory as the input file
        output_file_path = os.path.join(input_dir, f"{pdf_filename}.txt")
        
        # Convert PDF to a list of images
        images = convert_from_path(file_path)
        full_text = ""
        
        # OCR each image
        for i, image in enumerate(tqdm(images, desc=f"Processing {pdf_filename}", leave=False)):
            text = pytesseract.image_to_string(image, lang=lang)
            full_text += text + "\n"
        
        # Save the extracted text
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        
        return output_file_path
        
    except Exception as e:
        raise RuntimeError(f"Error processing {file_path}: {str(e)}")