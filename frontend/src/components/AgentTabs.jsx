import { useState } from "react";

const TAB_CONTENT = {
  Research: {
    title: "Research Agent",
    description:
      "Returns verified citation metadata from SerpAPI/Bing. No full prose.",
    items: [
      "Citation metadata only (title, authors, year, DOI/URL)",
      "Stores sources for APA formatting",
      "Flags missing evidence",
    ],
  },
  Critic: {
    title: "Critic Agent",
    description:
      "Challenges assumptions, identifies logical gaps, and asks questions.",
    items: [
      "Detects methodological weaknesses",
      "Highlights unsupported claims",
      "Requests stronger counterfactuals",
    ],
  },
  Synthesizer: {
    title: "Synthesizer Agent",
    description: "Builds outlines and argument structure only.",
    items: [
      "Creates thesis section scaffolding",
      "Maps claims to evidence",
      "Maintains logical flow",
    ],
  },
};

const TAB_KEYS = Object.keys(TAB_CONTENT);

export default function AgentTabs({ mode }) {
  const [active, setActive] = useState("Research");
  const tab = TAB_CONTENT[active];

  return (
    <div className="tabs">
      <div className="panel-header">
        <h2>Agent Workspace</h2>
        <span className="mode-pill">{mode.toUpperCase()}</span>
      </div>
      <div className="tab-buttons">
        {TAB_KEYS.map((key) => (
          <button
            key={key}
            type="button"
            className={key === active ? "active" : ""}
            onClick={() => setActive(key)}
          >
            {key}
          </button>
        ))}
      </div>
      <div className="tab-body">
        <h3>{tab.title}</h3>
        <p>{tab.description}</p>
        <ul>
          {tab.items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
        <div className="action-row">
          <button type="button">Run Agent</button>
          <button type="button" className="ghost">
            View Sources
          </button>
        </div>
      </div>
    </div>
  );
}
