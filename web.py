import streamlit as st
from PyPDF2 import PdfFileReader
from docx import Document

from main import content_analyzer


def read_txt(file):
    byte_content = file.getvalue()
    text = byte_content.decode("utf-8")
    return text


def read_docx(file):
    doc = Document(file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text


def read_pdf(file):
    text = ""
    with open(file, "rb") as f:
        reader = PdfFileReader(f)
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()
    return text


def main():
    st.title("File Content Reader")

    file = st.file_uploader("Upload a file", type=["docx", "pdf", "txt"])

    if file is not None:
        file_type = file.type

        if file_type == "application/pdf":
            text = read_pdf(file)
        elif (
            file_type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            text = content_analyzer(read_docx(file))
        elif file_type == "text/plain":

            with st.spinner("Analyzing ..."):
                text = content_analyzer(read_txt(file))

        else:
            st.error("Unsupported file type. Please upload a docx, pdf, or txt file.")

        st.header("File Content")
        st.text_input(label="Content Type:", value=text, disabled=True)
        st.success("Analyzed", icon="✅")


if __name__ == "__main__":
    main()
