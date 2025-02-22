from flask import Flask, render_template, request, send_file
import os
import PyPDF2

app = Flask(__name__) 

# Ensure 'uploads' directory exists
UPLOAD_FOLDER = "uploads" 
MERGED_PDF = "merged_output.pdf" 
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def merge_pdfs(pdf_list, output_filename):
    """Merge multiple PDFs into one."""
    merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_filename)
    merger.close()

@app.route("/", methods=["GET", "POST"]) 
def index():
    if request.method == "POST":
        uploaded_files = request.files.getlist("pdf_files")
        
        # Save uploaded files
        pdf_paths = []
        if len(uploaded_files) <= 1:
            return "Please upload more than one PDF to merge.", 400
        for file in uploaded_files:
            if file.filename == "":
                continue
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)
            pdf_paths.append(file_path)

        if pdf_paths:
            # Merge PDFs
            output_pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], MERGED_PDF)
            merge_pdfs(pdf_paths, output_pdf_path)
            return send_file(output_pdf_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
