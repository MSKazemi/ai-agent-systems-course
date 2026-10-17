# Safety, limitations and pre-deployment checks — ai-agent-systems-course

**Scope:** Instructional AI agent labs, MCP/A2A integrations and model-generated code execution demonstrations.  
**Issued:** 2026-10-17  
**Status:** Risk guidance only. No claim is made that any checklist item is already implemented, tested, legally approved or certified.

This document supplements [DISCLAIMER.md](DISCLAIMER.md) and the existing copyright/license terms without changing either. It does not prevent claims or waive mandatory legal duties.

## Risks to assess

- Teaching examples may execute generated code, access files or call external tools with the student's permissions.
- Untrusted prompts or remote tool content may trigger unsafe commands or leak tokens.
- Shared classroom Ollama endpoints and logs could contain learners' private prompts or other course data.

## Checks before live use

- [ ] Run code execution modules in disposable least-privilege containers or VMs with restricted network and filesystem access.
- [ ] Use dedicated non-production credentials, no secrets in course repos or example prompts, and rotate compromised keys.
- [ ] Keep student consent, privacy and classroom data retention arrangements clear before shared-service use.
- [ ] Document demonstrations as educational and unverified for production; never require students to disable platform protections.

## User and maintainer responsibilities

Begin in an isolated, authorized test environment; apply least privilege, backups, monitoring and an independent review of any high-impact outputs or actions. Where a project depends on third-party providers or real equipment, comply with vendor terms and safety instructions. Report suspected security flaws privately. Record actual test evidence, versions and unresolved risks rather than inferring that documentation is proof of implementation.

**Mandatory rights preserved:** Liability, product-safety, privacy, security and consumer obligations cannot be eliminated by this notice where applicable law forbids exclusion.
