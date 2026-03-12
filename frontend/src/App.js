import React, { useState } from "react";
import axios from "axios";

function App() {

  const [sessionId, setSessionId] = useState(null);
  const [question, setQuestion] = useState(null);
  const [feedback, setFeedback] = useState(null);

  const startQuiz = async () => {
    const res = await axios.post("http://127.0.0.1:8000/api/start-quiz/");
    const id = res.data.session_id;
    setSessionId(id);
    loadQuestion(id);
  };

  const loadQuestion = async (id) => {
    const res = await axios.get(`http://127.0.0.1:8000/api/question/${id}/`);
    setQuestion(res.data);
    setFeedback(null);
  };

  const submitAnswer = async (option) => {
    const res = await axios.post("http://127.0.0.1:8000/api/submit-answer/", {
      question_id: question.question_id,
      answer: option
    });

    setFeedback(res.data);
  };

  if (!sessionId) {
    return (
      <div style={{ textAlign: "center", marginTop: "120px" }}>
        <h1>AI Adaptive Quiz System</h1>
        <p>Test your aviation knowledge with AI generated questions.</p>
        <button
          onClick={startQuiz}
          style={{ padding: "12px 25px", fontSize: "16px" }}
        >
          Start Quiz
        </button>
      </div>
    );
  }

  if (!question) {
    return <h2 style={{ textAlign: "center" }}>Loading question...</h2>;
  }

  const difficulty =
    question.level <= 3
      ? "Easy"
      : question.level <= 6
      ? "Medium"
      : "Hard";

  const progress = (question.level / 10) * 100;

  return (
    <div style={{ width: "700px", margin: "auto", marginTop: "40px" }}>

      {/* Progress */}
      <div style={{ marginBottom: "20px" }}>
        <h2>Level {question.level} / 10</h2>
        <h3>Difficulty: {difficulty}</h3>

        <div
          style={{
            height: "10px",
            background: "#ddd",
            borderRadius: "5px",
            marginTop: "10px"
          }}
        >
          <div
            style={{
              width: `${progress}%`,
              height: "10px",
              background: "#4CAF50",
              borderRadius: "5px"
            }}
          ></div>
        </div>
      </div>

      {/* Question */}
      <div
        style={{
          padding: "20px",
          border: "1px solid #ddd",
          borderRadius: "8px"
        }}
      >
        <h3>{question.question}</h3>

        {Object.entries(question.options).map(([key, value]) => (
          <button
            key={key}
            onClick={() => submitAnswer(key)}
            style={{
              display: "block",
              width: "100%",
              marginTop: "10px",
              padding: "12px",
              fontSize: "15px"
            }}
          >
            {key}. {value}
          </button>
        ))}
      </div>

      {/* Feedback */}
      {feedback && (
        <div
          style={{
            marginTop: "25px",
            padding: "15px",
            border: "1px solid #ddd",
            borderRadius: "8px"
          }}
        >
          <h3>{feedback.correct ? "✅ Correct Answer" : "❌ Incorrect Answer"}</h3>

          <p>
            <b>Explanation:</b> {feedback.explanation}
          </p>

          <button
            onClick={() => loadQuestion(sessionId)}
            style={{
              marginTop: "10px",
              padding: "10px 20px",
              fontSize: "14px"
            }}
          >
            Next Question
          </button>
        </div>
      )}
    </div>
  );
}

export default App;