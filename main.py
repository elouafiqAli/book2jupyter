import random
import os
from PIL import Image
import fitz  # PyMuPDF
from pathlib import Path

SAMPLE_INPUT = "books/f1n503.pdf"
RANDOM_RANGE = [100, 300]

class AncientFrenchProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.output_dir = Path("processed_pages")
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_random_pages(self, random_range = RANDOM_RANGE):
        """Generate a random starting page and the next 10 pages"""
        start_page = random.randint(random_range[0],random_range[1])
        return list(range(start_page, start_page + 10))
    
    def convert_page_to_jpeg(self, page_num):
        """Convert a PDF page to JPEG"""
        doc = fitz.open(self.pdf_path)
        page = doc[page_num]
        
        # Get the pixel map
        pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
        
        # Save as JPEG
        output_path = self.output_dir / f"page_{page_num}.jpg"
        pix.save(str(output_path))
        
        doc.close()
        return output_path
    
    def process_with_gpt4(self, image_path):
        """
        Placeholder for GPT-4 processing
        In real implementation, this would call GPT-4 Vision API
        """
        # TODO: Implement actual GPT-4 Vision API call
        return f"Processed content for {image_path.name}\nThis is a placeholder for GPT-4 Vision API response."
    
    def save_text_result(self, image_path, text_content):
        """Save the processed text to a file"""
        text_path = image_path.with_suffix('.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        return text_path
    
    def process_pages(self):
        """Main processing function"""
        pages = self.generate_random_pages()
        results = []
        
        for page_num in pages:
            try:
                print(f"Processing page {page_num}...")
                
                # Convert to JPEG
                jpeg_path = self.convert_page_to_jpeg(page_num)
                print(f"Created JPEG: {jpeg_path}")
                
                # Process with GPT-4
                text_content = self.process_with_gpt4(jpeg_path)
                
                # Save result
                text_path = self.save_text_result(jpeg_path, text_content)
                print(f"Saved text result: {text_path}")
                
                results.append({
                    'page': page_num,
                    'jpeg': jpeg_path,
                    'text': text_path
                })
                
            except Exception as e:
                print(f"Error processing page {page_num}: {str(e)}")
        
        return results

if __name__ == "__main__":
    # Example usage
    processor = AncientFrenchProcessor(SAMPLE_INPUT)
    results = processor.process_pages()
    print("\nProcessing complete!")
    print("Processed pages:", [r['page'] for r in results])