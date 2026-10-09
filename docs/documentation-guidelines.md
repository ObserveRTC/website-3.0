# ObserveRTC documentation guidelines

Approved documentation structure: section → page, with at most two navigation
levels. Architecture belongs in Overview. Write for engineers integrating and
operating ObserveRTC, while retaining useful implementation detail.

Motto: **From Signals to Insights.**

Primary editorial references:
- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
- [Google developer documentation style guide](https://developers.google.com/style)

## Purpose and audience

Every page helps a reader understand a concept, evaluate a capability, implement
something, investigate a problem, or find a technical contract. Explain what
matters, show how it works, and link to deeper evidence. Documentation is not a
transcription of internal classes.

Use the same authoritative documentation for humans and coding agents.

## Information architecture

The primary sections are Overview, Getting started, Concepts, Client Monitor,
Observer, Schemas, Codecs, Guides, and Reference. Use no third-level sidebar groups.
Keep schema history reachable from compatibility pages without recursively listing
it in navigation. Preserve existing published URLs or provide aliases.

Component sections retain detailed APIs, configuration, metrics, events, issues,
detectors, and runtime behavior. Explain each implementation detail through the
integration decision or consequence it helps an engineer understand.

Guides are organized by tasks and symptoms. Each guide links to the relevant
concept and component contract instead of reproducing their full content. Overview
contains the ecosystem architecture; collection, ingestion, and scoring pages
contain the deeper processing behavior. Do not create empty categories.

## Clear writing

Use active voice, present tense, second person, precise terms, and short focused
paragraphs. Prefer concrete statements to adjectives, promotional claims, or
ambiguous pronouns. Titles and headings use sentence case; package/product names
keep their official capitalization. Headings are plain text; identifiers in prose
use inline code. Use descriptive action headings for tasks and noun phrases for
concepts. Maintain a logical heading hierarchy.

## Page structures

Select the structure that fits the page rather than imposing one template.

- Component: purpose, why it exists, capabilities, conceptual processing flow,
  useful example, integration decisions, runtime behavior, limitations, next steps.
- Concept: definition, motivation, behavior, practical example, distinctions and
  limitations, related contracts.
- Guide: goal, prerequisites, ordered procedure, expected result, troubleshooting,
  related references.
- Reference: API name/purpose, signature or schema, parameters/types, returns or
  events, semantics, defaults/constraints, errors/edge cases, example, source.
- Troubleshooting: symptom, confirmation, possible causes, diagnostic procedure,
  expected evidence, resolution, related documentation. Possible causes are not
  confirmed diagnoses.

Reusable starting points live in `archetypes/docs/`. Replace prompts with real
content before publishing; no placeholder page should enter navigation.

## Examples and evidence

Use real supported APIs and include imports, required initialization, meaningful
inputs, and expected results. Explain variables supplied by the host application.
Verify signatures and semantics against the release source; run executable examples
where practical. Do not describe source inspection as runtime verification.

Install examples normally omit version pins, but identify release coverage for
version-sensitive behavior. Do not infer current behavior from historical snapshots.
Never present proposals or design discussions as shipped capabilities.

Evidence priority:
1. Public interfaces and implementation.
2. Automated tests.
3. Published schemas and package definitions.
4. Official WebRTC specifications (W3C and IETF).
5. Maintained project documentation.
6. Design discussions and proposals.

Link important technical claims to appropriate sources. Prefer stable revision
links. Distinguish standard semantics, browser availability, and ObserveRTC behavior.

## Telemetry contracts

`content/docs/concepts/telemetry.md` is the authoritative glossary. Use its terms
consistently: raw statistics, adapted statistics, derived metrics, detectors,
issues, quality scores, events, and session-level evaluations.

Each metric reference identifies unit, scope, source, interpretation, and missing
input behavior. Each detector explains input signals, evaluation, output/lifecycle,
and limitations. Scores identify aggregation and missing-data semantics.

## Progressive disclosure and accessibility

Explain purpose first, implementation second, detailed investigation third. Link
between levels rather than filling introductory pages with internal mechanics.
Maintainable text diagrams or diagrams-as-code must have a concise explanation and
text alternative. Essential information must remain available in source and rendered
content even when visually placed in expandable details.

Markdown outputs and `llms.txt` are generated from the same documentation. The
agent index links to authoritative pages; it must not become a second contract.

## Maintenance and acceptance

Update docs with relevant behavior changes; generate references where practical.
Check examples, local links, external source links, version coverage, and navigation.
Mark experimental behavior explicitly, and remove/archive obsolete content.
Component maintainers own technical contracts; website maintainers own presentation,
navigation, and link/output checks.

Before completion, confirm:
- Each page has an audience and purpose.
- Component behavior is understandable without reading source.
- Getting started reaches a meaningful observed result.
- Guides support concrete engineering tasks.
- References are precise and source-backed.
- Terminology and version claims are consistent.
- Detailed behavior is available without overwhelming introductions.
- Humans and agents can access the same authoritative content.
- Content remains maintainable without duplicated contracts.
