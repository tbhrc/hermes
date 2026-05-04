HERMES_HOME=/root/3_core_tools/hermes/data/ (already set via env var). This is the canonical AOS Hub location — native, not symlinked. Always reference files directly as /root/3_core_tools/hermes/data/... NEVER through ~/.hermes/. I am part of the core tools ecosystem (3_core_tools/). File organization must be human-readable and logical — follow AOS Hub's 12-pillar structure (AGENTS.md). Be organized in folder creation and file saving, maintaining consistency with David's structured approach. The symlink at ~/.hermes/ is legacy — ignore it.

A1 Hermes Profile Location (verified 2026-05-03):
- ACTUAL DATA: /root/1_command/1.1_orchestrator/hermes_profile/ (pillar structure - authoritative)
- SYMLINK: /root/.hermes/profiles/a1 → /root/1_command/1.1_orchestrator/hermes_profile/
- DOCUMENTATION: /root/1_command/1.1_orchestrator/A1_HERMES_PROFILE.md
- WRAPPER: a1 (calls hermes -p a1, follows symlink to pillar)
- Profile cannot be in hidden folder — must be accessible from AOS Hub pillar structure.
§
Task tracking: Persistent tasks/ folder deleted per user action. Only session-scoped todo tool remains (no cross-session persistence). Governance protocol: when user mentions new/updated governance files (AGENTS.md, RULES.md), immediately read and report contents to confirm operational policy understanding.
§
Secrets Management Procedure: All secrets/API keys stored in /root/.env (ROOT), not in Hermes data folder. Anytime we have new secrets, add to /root/.env. Never share secrets in chat or request them via messaging platforms. Read tokens from /root/.env programmatically when needed. OPENAI_API_KEY_AOS is the A1/Orchestrator prioritized key.
§
User verified Pinecone Starter free (1 index, 2GB, 100k vectors, no CC) via full page extract of https://www.pinecone.io/pricing/, initial paid SaaS assessment wrong. Multi-layer memory needs vector DB, open source (Chroma/Weaviate/Qdrant) or free tier, consolidation (dreaming). Wake-up: agents read /root/3_core_tools/hermes/data/AGENTS.md first.
§
Firecrawl is being self-hosted by H1 (another agent) for AOS Hub use, no install needed from our side.