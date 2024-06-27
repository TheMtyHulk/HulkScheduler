from pypdf import PdfReader, PdfWriter
import pymongo
from gridfs import GridFS
import os

class CompressPDF:
    def __init__(self,task_id,worker_id) -> None:
        client = pymongo.MongoClient(os.getenv('MONGO_URL'))
        db = client["taskmaster"]
        fs = GridFS(db)
        self.worker_id=worker_id
        self.file = fs.find_one({"_id":task_id})
        if self.file:
            # Save the PDF file locally
            self.save_path = "worker_files/"+self.file.filename
            with open(self.save_path, "wb") as f:
                f.write(self.file.read())
        else:
            print("File not found.")
        pass
    
    def compressPDF(self):
        reader = PdfReader(self.save_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        name = self.file.filename[:-4]
        for page in writer.pages:
            for img in page.images:
                img.replace(img.image, quality=30)
                page.compress_content_streams()
        compressed_path = name + " compressed_ by_"+str(self.worker_id)+".pdf"
        
        output_path = "worker_files/"+compressed_path
        with open(output_path, "wb") as f:
            writer.write(f)
        
        # Delete the original file used to compress
        if os.path.exists(self.save_path):
            os.remove(self.save_path)
        else:
            print("Original file not found.")
        
        return

# c=CompressPDF("8839f99d-f392-4be9-8c0a-2659fb21ce41")
# c.compressPDF()
# Connect to MongoDB


# Access the GridFS collection


# Retrieve the PDF file by its filename
# filename = "testfiles/filetest on mongo/file upload/syllabus.pdf"


# Check if the file exists

    
    