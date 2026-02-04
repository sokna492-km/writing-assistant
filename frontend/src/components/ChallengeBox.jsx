const QUESTIONS = [
  "What is your core definition of M&A success?",
  "Which industries, geographies, and time periods are included?",
  "How will you address selection bias in deal completion?",
  "What counterfactuals strengthen your causal claims?",
];

export default function ChallengeBox({ mode }) {
  return (
    <div className="challenge-box">
      <div>
        <p className="eyebrow">Challenge Box</p>
        <h2>Answer these questions before receiving suggestions</h2>
      </div>
      <div className="challenge-content">
        <ul>
          {QUESTIONS.map((question) => (
            <li key={question}>{question}</li>
          ))}
        </ul>
        <div className="challenge-meta">
          <span>Mode: {mode}</span>
          <button type="button">Submit Answers</button>
        </div>
      </div>
    </div>
  );
}
