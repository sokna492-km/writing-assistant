import { useState } from "react";
import AgentTabs from "./components/AgentTabs.jsx";
import ChallengeBox from "./components/ChallengeBox.jsx";
import Editor from "./components/Editor.jsx";

const MODES = [
  { label: "Default", value: "default" },
  { label: "Socratic Mode", value: "socratic" },
  { label: "Review Mode", value: "review" },
  { label: "Structure Mode", value: "structure" },
];

export default function App() {
  const [mode, setMode] = useState("default");

  return (
    <div className="page">
      <header className="header">
        <div>
          <p className="eyebrow">M&A Thesis Thinking Assistant</p>
          <h1>Multi-agent workspace for research, critique, and structure</h1>
        </div>
        <div className="mode-select">
          <label htmlFor="mode">Mode</label>
          <select
            id="mode"
            value={mode}
            onChange={(event) => setMode(event.target.value)}
          >
            {MODES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </header>

      <main className="content">
        <section className="panel left">
          <Editor />
        </section>
        <section className="panel right">
          <AgentTabs mode={mode} />
        </section>
      </main>

      <footer className="challenge">
        <ChallengeBox mode={mode} />
      </footer>
    </div>
  );
}
