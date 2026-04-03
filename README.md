paralegal-lk-internship-assignment

//Setup
cd paralegal-lk-internship-assignment
uv sync

//Running
uv run python main.py

//Approach
I used pdfplumber to extract text from each PDF file. For the bench, I searched for the "Before:" keyword and extracted the names that followed it. For the author judge, I attempted to identify the judge who delivered the judgment using pattern matching but was unable to complete a reliable implementation.
