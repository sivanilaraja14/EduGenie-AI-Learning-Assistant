# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project
documentation. It uses FastAPI for the backend, HTML/CSS/JavaScript for the
frontend, Google Gemini for Q&A, quiz generation, summarization and learning
recommendations, and LaMini-Flan-T5-783M for concept explanations.

## Features

- Ask educational questions
- Explain concepts simply
- Generate exactly 3 MCQs with 4 options each
- Summarize educational text
- Generate beginner-to-advanced learning paths
- Interactive quiz answer checking in the browser
- `/health` endpoint for a quick backend check

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
└── tests/
    └── test_api.py
```

## 1. Prerequisites

The project documentation specifies Python 3.10+.

Verify:

```powershell
python --version
```

On Windows, if `python` is unavailable, try:

```powershell
py --version
```

## 2. Open the project in VS Code

Open the `EduGenie` folder in VS Code.

Open the integrated terminal:

```text
Terminal -> New Terminal
```

## 3. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The first use of the local explanation feature can download the
`MBZUAI/LaMini-Flan-T5-783M` model from Hugging Face. That model is much
larger than the application source code, so the first explanation request
may take longer.

## 5. Configure Gemini

Copy:

```text
.env.example
```

to:

```text
.env
```

Then set:

```env
GEMINI_API_KEY=your_real_key_here
```

The supplied documentation specifies Gemini 1.5 Pro. The code therefore uses
`gemini-1.5-pro` as the default configured model. If that model is no longer
available to your Google AI API project, change `GEMINI_MODEL` in `.env` to a
currently available Gemini model.

Never commit `.env` to Git.

## 6. Run the application

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

The supplied documentation also specifies this Uvicorn command and local URL.

## 7. Test the API

Health check:

```text
GET http://127.0.0.1:8000/health
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## 8. Functional testing

### Q&A

Enter:

```text
Which is the largest ocean?
```

Expected behavior: EduGenie returns an educational answer.

### Explanation

Enter:

```text
Pythagoras theorem
```

Expected behavior: EduGenie gives a beginner-friendly explanation.

### Quiz

Enter:

```text
The Pythagorean theorem relates the sides of a right-angled triangle.
```

Expected behavior:
- exactly 3 questions
- exactly 4 options per question
- one correct answer per question
- browser-side answer checking

### Summary

Paste a long educational paragraph.

Expected behavior: the important information is condensed into a clearer,
shorter summary.

### Learning path

Enter:

```text
SQL
```

Expected behavior: a beginner-to-advanced learning path with topics,
estimated time, practice guidance and resource types.

## 9. Run automated tests

```bash
pytest -q
```

These tests cover application startup, the health endpoint and quiz output
validation without making a paid/external Gemini request.

## API design

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Web application |
| `/health` | GET | Health check |
| `/qa` | POST | Question answering |
| `/explain` | POST | Concept explanation |
| `/quiz` | POST | Three-question MCQ generation |
| `/summarize` | POST | Text summarization |
| `/learn/recommendations` | GET | Learning path generation |
| `/docs` | GET | FastAPI Swagger UI |

## Implementation notes

The source document gives the architecture, modules, model choices, endpoint
names and UI behavior, but it does not provide complete source code or exact
request/response schemas. This implementation fills those missing engineering
details with typed Pydantic request models, error handling, JSON validation,
a browser-side quiz renderer, a health endpoint and automated tests.

The supplied document's screenshots show separate task areas, while its
architecture describes a task dropdown. This implementation combines both
ideas into a single responsive task selector while retaining all five
documented capabilities.

For production use, add authentication, rate limiting, structured logging,
request IDs, secret management, model timeouts/retries, and monitoring.
