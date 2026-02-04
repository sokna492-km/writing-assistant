from typing import Dict, List

from langgraph.graph import StateGraph

from app.agents.prompts import (
    CRITIC_AGENT_PROMPT,
    MODE_GUIDANCE,
    RESEARCH_AGENT_PROMPT,
    SYNTHESIZER_AGENT_PROMPT,
)
from app.schemas import AgentRequest, AgentResponse, Mode


class AssistantState(Dict[str, str]):
    pass


def _apply_mode_guidance(role_prompt: str, mode: Mode) -> str:
    guidance = MODE_GUIDANCE[mode.value]
    return f"{role_prompt.strip()}\nMode guidance: {guidance}"


def _research_node(state: AssistantState) -> AssistantState:
    prompt = state["prompt"]
    mode = state["mode"]
    role_prompt = _apply_mode_guidance(RESEARCH_AGENT_PROMPT, mode)
    state["research"] = (
        f"{role_prompt}\n\nQuery: {prompt}\n"
        "[Stub] Connect to SerpAPI/Bing and return citation metadata only."
    )
    return state


def _critic_node(state: AssistantState) -> AssistantState:
    prompt = state["prompt"]
    mode = state["mode"]
    role_prompt = _apply_mode_guidance(CRITIC_AGENT_PROMPT, mode)
    state["critic"] = (
        f"{role_prompt}\n\nFocus: {prompt}\n"
        "- What assumptions about M&A value creation need evidence?\n"
        "- Which industries/periods are excluded and why?\n"
        "- What counterfactuals will you use?"
    )
    return state


def _synthesizer_node(state: AssistantState) -> AssistantState:
    prompt = state["prompt"]
    mode = state["mode"]
    role_prompt = _apply_mode_guidance(SYNTHESIZER_AGENT_PROMPT, mode)
    state["synthesizer"] = (
        f"{role_prompt}\n\nThesis focus: {prompt}\n"
        "1. Introduction\n"
        "   - Motivation\n"
        "   - Research questions\n"
        "2. Literature Review\n"
        "3. Data & Methodology\n"
        "4. Results & Robustness\n"
        "5. Discussion & Implications\n"
        "6. Conclusion"
    )
    return state


def _challenge_questions(prompt: str) -> List[str]:
    return [
        "What is the precise definition of M&A success in your thesis?",
        "Which data sources will provide merger outcomes and why?",
        "How will you address selection bias in completed deals?",
        f"What is the strongest counterargument to: {prompt}?",
    ]


class AssistantOrchestrator:
    def __init__(self) -> None:
        graph = StateGraph(AssistantState)
        graph.add_node("research", _research_node)
        graph.add_node("critic", _critic_node)
        graph.add_node("synthesizer", _synthesizer_node)
        graph.set_entry_point("research")
        graph.add_edge("research", "critic")
        graph.add_edge("critic", "synthesizer")
        graph.set_finish_point("synthesizer")
        self._graph = graph.compile()

    def run(self, request: AgentRequest) -> AgentResponse:
        state: AssistantState = {
            "prompt": request.prompt,
            "mode": request.mode,
        }
        result = self._graph.invoke(state)
        return AgentResponse(
            mode=request.mode,
            research=result.get("research"),
            critic=result.get("critic"),
            synthesizer=result.get("synthesizer"),
            challenge_questions=_challenge_questions(request.prompt),
            citations=request.citations,
        )
