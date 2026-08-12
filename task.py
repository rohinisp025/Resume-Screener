import fitz  # PyMuPDF
import docx
from agent import analyze_resume


# -----------------------------
# Read PDF Resume
# -----------------------------
def read_pdf(uploaded_file):
    text = ""

    pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


# -----------------------------
# Read DOCX Resume
# -----------------------------
def read_docx(uploaded_file):
    doc = docx.Document(uploaded_file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


# -----------------------------
# Extract Resume Text
# -----------------------------
def extract_resume(uploaded_file):

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return read_pdf(uploaded_file)

    elif filename.endswith(".docx"):
        return read_docx(uploaded_file)

    else:
        raise Exception("Only PDF and DOCX files are supported.")


# -----------------------------
# Resume Screening Task
# -----------------------------
def resume_screening(uploaded_resume, job_description):

    resume_text = extract_resume(uploaded_resume)

    result = analyze_resume(
        resume_text,
        job_description
    )

    return result