from fastapi import FastAPI, UploadFile, File

import PyPDF2

from io import BytesIO



app = FastAPI()



# Root endpoint

@app.get("/")

def read_root():

    return {"message": "Welcome to StudyMate Backend!"}



# Upload PDF endpoint

@app.post("/uploadpdf/")

async def upload_pdf(file: UploadFile = File(...)):

    try:

        # Read uploaded PDF

        content = await file.read()

        pdf_reader = PyPDF2.PdfReader(BytesIO(content))

        text = ""

        for page in pdf_reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text



        # Save the uploaded PDF in backend folder

        with open(file.filename, "wb") as f:

            f.write(content)



        # Return first 500 characters of text

        return {"filename": file.filename, "size": len(content), "text": text[:500]}

    except Exception as e:

        return {"error": str(e)}



# Ask question endpoint (returns snippet)

@app.get("/ask/")

def ask_question(filename: str, question: str):

    try:

        from PyPDF2 import PdfReader



        # Open PDF

        with open(filename, "rb") as f:

            pdf_reader = PdfReader(f)

            text = ""

            for page in pdf_reader.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text



        # Find relevant snippet

        if question.lower() in text.lower():

            index = text.lower().find(question.lower())

            start = max(index - 50, 0)

            end = min(index + 50, len(text))

            snippet = text[start:end]

            return {"answer": snippet}

        else:

            return {"answer": "The PDF does not contain this text."}



    except Exception as e:

        return {"error": str(e)}
