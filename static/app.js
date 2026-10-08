const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const inputLabel = document.getElementById("inputLabel");
const submitButton = document.getElementById("submitButton");
const resultCard = document.getElementById("resultCard");
const resultTitle = document.getElementById("resultTitle");
const result = document.getElementById("result");
const status = document.getElementById("status");

const taskConfig = {
    qa: {
        label: "Your question",
        placeholder: "e.g. Which is the largest ocean?",
        button: "Get Answer",
    },
    explain: {
        label: "Topic to explain",
        placeholder: "e.g. Pythagoras theorem",
        button: "Explain",
    },
    quiz: {
        label: "Topic or passage",
        placeholder: "Paste a passage or enter a topic for a 3-question quiz.",
        button: "Generate Quiz",
    },
    summarize: {
        label: "Text to summarize",
        placeholder: "Paste a long educational passage here.",
        button: "Summarize",
    },
    learn: {
        label: "Learning topic",
        placeholder: "e.g. SQL",
        button: "Get Recommendations",
    },
};

function updateTaskUI() {
    const config = taskConfig[task.value];

    inputLabel.textContent = config.label;
    inputText.placeholder = config.placeholder;
    submitButton.textContent = config.button;
}

task.addEventListener("change", updateTaskUI);
updateTaskUI();


/*
 * Convert Gemini Markdown-style output into safe HTML.
 *
 * This handles:
 * - **bold**
 * - *italic*
 * - headings
 * - bullet lists
 * - numbered lists
 * - horizontal lines
 * - paragraphs
 */
function renderMarkdown(text) {
    if (!text) {
        return "";
    }

    // Escape HTML first for safety.
    let html = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

    // Normalize escaped Markdown returned by the model.
    html = html.replace(/\\\*/g, "*");
    html = html.replace(/\\#/g, "#");
    html = html.replace(/\\-/g, "-");

    // Horizontal rules.
    html = html.replace(
        /^\s*---+\s*$/gm,
        "<hr>"
    );

    // Headings.
    html = html.replace(
        /^### (.+)$/gm,
        "<h4>$1</h4>"
    );

    html = html.replace(
        /^## (.+)$/gm,
        "<h3>$1</h3>"
    );

    html = html.replace(
        /^# (.+)$/gm,
        "<h2>$1</h2>"
    );

    // Bold + italic.
    html = html.replace(
        /\*\*(.+?)\*\*/g,
        "<strong>$1</strong>"
    );

    html = html.replace(
        /\*(.+?)\*/g,
        "<em>$1</em>"
    );

    // Numbered lists.
    html = html.replace(
        /(?:^|\n)(\d+\.\s.+(?:\n\d+\.\s.+)*)/g,
        (match) => {
            const items = match
                .trim()
                .split("\n")
                .map(item => {
                    return item.replace(
                        /^\d+\.\s+/,
                        ""
                    );
                })
                .map(item => `<li>${item}</li>`)
                .join("");

            return `<ol>${items}</ol>`;
        }
    );

    // Bullet lists.
    html = html.replace(
        /(?:^|\n)((?:[-*]\s.+\n?)+)/g,
        (match) => {
            const items = match
                .trim()
                .split("\n")
                .map(item => {
                    return item.replace(
                        /^[-*]\s+/,
                        ""
                    );
                })
                .map(item => `<li>${item}</li>`)
                .join("");

            return `<ul>${items}</ul>`;
        }
    );

    // Convert remaining newlines into paragraphs/breaks.
    html = html
        .split(/\n{2,}/)
        .map(paragraph => {
            const trimmed = paragraph.trim();

            if (!trimmed) {
                return "";
            }

            if (
                trimmed.startsWith("<h") ||
                trimmed.startsWith("<ul") ||
                trimmed.startsWith("<ol") ||
                trimmed.startsWith("<hr")
            ) {
                return trimmed;
            }

            return `<p>${trimmed.replace(/\n/g, "<br>")}</p>`;
        })
        .join("");

    return html;
}


function showError(message) {
    resultCard.classList.remove("hidden");

    resultTitle.textContent = "Error";
    status.textContent = "";

    result.textContent = message;
}


function showLoading() {
    resultCard.classList.remove("hidden");

    resultTitle.textContent = "Working...";
    status.textContent = "AI is generating your result";

    result.textContent = "Please wait...";
}


function renderAIText(title, text) {
    resultTitle.textContent = title;

    result.innerHTML = renderMarkdown(text);
}


function renderQuiz(quiz) {
    resultTitle.textContent = "Quiz";
    status.textContent = "3 questions";

    const wrapper = document.createElement("div");

    quiz.forEach((item, index) => {
        const question = document.createElement("div");

        question.className = "quiz-question";

        const title = document.createElement("h3");

        title.textContent =
            `Q${index + 1}. ${item.question}`;

        question.appendChild(title);

        const options = document.createElement("div");

        options.className = "quiz-options";

        item.options.forEach((option, optionIndex) => {
            const label = document.createElement("label");

            const radio = document.createElement("input");

            radio.type = "radio";
            radio.name = `q-${index}`;
            radio.value = option;

            label.appendChild(radio);

            label.append(
                ` ${String.fromCharCode(65 + optionIndex)}. ${option}`
            );

            options.appendChild(label);
        });

        const check = document.createElement("button");

        check.type = "button";
        check.textContent = "Check Answer";

        const feedback = document.createElement("div");

        feedback.className = "feedback";

        check.addEventListener("click", () => {
            const selected = document.querySelector(
                `input[name="q-${index}"]:checked`
            );

            if (!selected) {
                feedback.textContent =
                    "Please select an option.";

                feedback.className =
                    "feedback wrong";

                return;
            }

            if (selected.value === item.answer) {
                feedback.textContent =
                    "✓ Correct!";

                feedback.className =
                    "feedback correct";
            } else {
                feedback.textContent =
                    `✗ Incorrect. Correct answer: ${item.answer}`;

                feedback.className =
                    "feedback wrong";
            }
        });

        question.appendChild(options);
        question.appendChild(check);
        question.appendChild(feedback);

        wrapper.appendChild(question);
    });

    result.replaceChildren(wrapper);
}


async function submitTask() {
    const value = inputText.value.trim();

    if (!value) {
        showError("Please enter some content first.");
        return;
    }

    showLoading();

    submitButton.disabled = true;

    try {
        let response;

        if (task.value === "qa") {
            response = await fetch("/qa", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    question: value,
                }),
            });

        } else if (task.value === "explain") {
            response = await fetch("/explain", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    topic: value,
                }),
            });

        } else if (task.value === "quiz") {
            response = await fetch("/quiz", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    text: value,
                }),
            });

        } else if (task.value === "summarize") {
            response = await fetch("/summarize", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    text: value,
                }),
            });

        } else {
            response = await fetch(
                `/learn/recommendations?topic=${encodeURIComponent(value)}`
            );
        }


        /*
         * Read the response safely.
         *
         * This also prevents the previous:
         * "Unexpected token I ... is not valid JSON"
         * error when the backend returns a non-JSON error.
         */
        const responseText = await response.text();

        let data;

        try {
            data = JSON.parse(responseText);
        } catch {
            throw new Error(
                response.ok
                    ? "The server returned an invalid response."
                    : `Server error (${response.status}): ${responseText}`
            );
        }


        if (!response.ok) {
            const detail =
                data.detail ||
                "The request failed.";

            throw new Error(
                Array.isArray(detail)
                    ? detail
                        .map(item => item.msg)
                        .join(", ")
                    : detail
            );
        }


        resultCard.classList.remove("hidden");

        status.textContent = "Complete";


        if (task.value === "qa") {

            renderAIText(
                "Answer",
                data.answer
            );

        } else if (task.value === "explain") {

            renderAIText(
                "Explanation",
                data.explanation
            );

        } else if (task.value === "quiz") {

            renderQuiz(data.quiz);

        } else if (task.value === "summarize") {

            renderAIText(
                "Summary",
                data.summary
            );

        } else {

            renderAIText(
                "Learning Recommendations",
                data.recommendation
            );
        }

    } catch (error) {

        showError(
            error.message ||
            "Something went wrong."
        );

    } finally {

        submitButton.disabled = false;
    }
}


submitButton.addEventListener(
    "click",
    submitTask
);