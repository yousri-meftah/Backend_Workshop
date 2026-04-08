from fastapi import HTTPException


QUIZ_SESSION = {
    "id": 1,
    "title": "Backend Session Warmup",
    "description": "15 workshop questions on DNS, HTTPS, HTTP methods, APIs, and backend fundamentals.",
    "topic": "Backend Basics",
}

QUIZ_QUESTIONS = [
    {
        "position": 1,
        "question": "What does DNS mainly do on the internet?",
        "options": {
            "A": "Encrypt the data between the browser and the server",
            "B": "Translate a domain name into an IP address",
            "C": "Store frontend files in the browser cache",
            "D": "Create database tables for an application",
        },
        "correct_option": "B",
    },
    {
        "position": 2,
        "question": "Which protocol is commonly used to load a secure website?",
        "options": {
            "A": "FTP",
            "B": "SMTP",
            "C": "HTTPS",
            "D": "SSH",
        },
        "correct_option": "C",
    },
    {
        "position": 3,
        "question": "What is the main purpose of HTTPS?",
        "options": {
            "A": "To compress JSON responses",
            "B": "To make a site faster than all HTTP requests",
            "C": "To secure communication with encryption and certificate validation",
            "D": "To replace DNS records",
        },
        "correct_option": "C",
    },
    {
        "position": 4,
        "question": "Which HTTP method is usually used to create a new resource?",
        "options": {
            "A": "GET",
            "B": "POST",
            "C": "DELETE",
            "D": "HEAD",
        },
        "correct_option": "B",
    },
    {
        "position": 5,
        "question": "Which HTTP method should be used to fetch data without changing it?",
        "options": {
            "A": "GET",
            "B": "PATCH",
            "C": "PUT",
            "D": "DELETE",
        },
        "correct_option": "A",
    },
    {
        "position": 6,
        "question": "Which HTTP method is commonly used to fully replace an existing resource?",
        "options": {
            "A": "PUT",
            "B": "TRACE",
            "C": "OPTIONS",
            "D": "CONNECT",
        },
        "correct_option": "A",
    },
    {
        "position": 7,
        "question": "Which HTTP method is commonly used to partially update a resource?",
        "options": {
            "A": "POST",
            "B": "PATCH",
            "C": "GET",
            "D": "HEAD",
        },
        "correct_option": "B",
    },
    {
        "position": 8,
        "question": "What does a `404` response usually mean?",
        "options": {
            "A": "The user is not logged in",
            "B": "The server crashed during startup",
            "C": "The requested resource was not found",
            "D": "The browser sent invalid JSON",
        },
        "correct_option": "C",
    },
    {
        "position": 9,
        "question": "What does a `500` response usually mean?",
        "options": {
            "A": "There is a server-side error",
            "B": "The request was successful",
            "C": "The client must log in again",
            "D": "The DNS lookup failed",
        },
        "correct_option": "A",
    },
    {
        "position": 10,
        "question": "Why do APIs commonly use JSON?",
        "options": {
            "A": "It can only be read by Python servers",
            "B": "It is a lightweight format that is easy for clients and servers to exchange",
            "C": "It automatically encrypts passwords",
            "D": "It replaces SQL in databases",
        },
        "correct_option": "B",
    },
    {
        "position": 11,
        "question": "What is an API endpoint?",
        "options": {
            "A": "A CSS class used by frontend pages",
            "B": "A specific URL path where a backend exposes a resource or action",
            "C": "A local database backup file",
            "D": "A command that only works in Swagger",
        },
        "correct_option": "B",
    },
    {
        "position": 12,
        "question": "What is the role of a backend server in a web app?",
        "options": {
            "A": "Only designing the page colors",
            "B": "Only registering domain names",
            "C": "Handling business logic, data storage, and API responses",
            "D": "Replacing the user's browser",
        },
        "correct_option": "C",
    },
    {
        "position": 13,
        "question": "What is the main difference between SQL and NoSQL databases?",
        "options": {
            "A": "SQL uses structured tables, while NoSQL uses flexible data models",
            "B": "SQL is faster than NoSQL in all cases",
            "C": "NoSQL only works on Windows",
            "D": "SQL cannot store data"
        },
        "correct_option": "A"
    },
    {
        "position": 14,
        "question": "Why is validation important on the backend?",
        "options": {
            "A": "It lets CSS load faster",
            "B": "It checks incoming data before using or storing it",
            "C": "It removes the need for a database",
            "D": "It makes every request idempotent",
        },
        "correct_option": "B",
    },
    {
        "position": 15,
        "question": "What is Swagger mainly useful for in this workshop app?",
        "options": {
            "A": "Writing SQL migrations automatically",
            "B": "Hosting static HTML pages",
            "C": "Exploring and testing API endpoints from generated documentation",
            "D": "Creating SSL certificates",
        },
        "correct_option": "C",
    },
]


def get_quiz_session_or_404(session_id: int):
    if session_id != QUIZ_SESSION["id"]:
        raise HTTPException(status_code=404, detail="Quiz session not found")
    return {
        **QUIZ_SESSION,
        "question_count": len(QUIZ_QUESTIONS),
    }


def get_quiz_question_by_position_or_404(session_id: int, question_position: int):
    get_quiz_session_or_404(session_id)
    for item in QUIZ_QUESTIONS:
        if item["position"] == question_position:
            return {
                "position": item["position"],
                "question": item["question"],
                "options": [
                    {"key": "A", "text": item["options"]["A"]},
                    {"key": "B", "text": item["options"]["B"]},
                    {"key": "C", "text": item["options"]["C"]},
                    {"key": "D", "text": item["options"]["D"]},
                ],
                "correct_option": item["correct_option"],
            }
    raise HTTPException(status_code=404, detail="Quiz question not found")
