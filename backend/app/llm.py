from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from environment

ASSESS_SYSTEM = """You are an eligibility assessment engine for social support.
Return strict JSON:
{
  "decision":"approve|soft_decline|needs_more_info",
  "confidence": 0.0-1.0,
  "reasons": ["..."],
  "criteria": {
    "income_level":"meets|borderline|fails",
    "employment_history":"stable|unstable|unknown",
    "family_size":"small|medium|large",
    "wealth":"low|medium|high|unknown",
    "demographic_profile":"at_risk|standard|unknown"
  },
  "evidence_citations": ["..."]
}
Only JSON."""

RECS_SYSTEM = """Return JSON:
{
  "upskilling":[{"title":"", "provider":"", "link":""}],
  "jobs":[{"title":"", "industry":"", "why_match":""}],
  "counseling":[{"type":"career|financial", "note":""}]
}
Only JSON."""

CHAT_SYSTEM = """Helpful support assistant. Be concise and safe. If asked about decisions,
encourage contacting the case officer for official confirmation."""

def _responses_json(system_prompt: str, user_prompt: str, model: str = "gpt-4o-mini") -> str:
    r = client.responses.create(
        model=model,
        input=[
            {"role":"system","content":[{"type":"text","text":system_prompt}]},
            {"role":"user","content":[{"type":"text","text":user_prompt}]},
        ],
        temperature=0.2,
        response_format={"type":"json_object"}
    )
    return getattr(r, "output_text", None) or r.output[0].content[0].text

def _responses_text(system_prompt: str, user_prompt: str, model: str = "gpt-4o-mini") -> str:
    r = client.responses.create(
        model=model,
        input=[
            {"role":"system","content":[{"type":"text","text":system_prompt}]},
            {"role":"user","content":[{"type":"text","text":user_prompt}]},
        ],
        temperature=0.3,
    )
    return getattr(r, "output_text", None) or r.output[0].content[0].text

def assess_json(user_payload: str) -> str:
    return _responses_json(ASSESS_SYSTEM, user_payload)

def recs_json(user_payload: str) -> str:
    return _responses_json(RECS_SYSTEM, user_payload)

def chat_text(user_payload: str) -> str:
    return _responses_text(CHAT_SYSTEM, user_payload)
