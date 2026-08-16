---
title: "Code generation & versioning"
slug: "general"
description: "How the ObserveRTC schema generator works and how versions are managed"
lead: "Avro sources in, TypeScript / protobuf / Markdown bindings out"
date: 2023-09-07T16:33:54+02:00
lastmod: 2026-08-16T10:00:00+02:00
draft: false
weight: 210
toc: true
---

**Repository:** [github.com/observertc/schemas](https://github.com/observertc/schemas)

## The pipeline

Avro schema definitions in `sources/samples/` are the single source of truth. A TypeScript CLI
reads them, validates them, and writes every other artifact.

```bash
git clone https://github.com/observertc/schemas.git
cd schemas
npm install
npm run generate
```

That one command:

{{< steps >}}
{{< step >}}Reads and validates the Avro schema files in `sources/samples/`.{{< /step >}}
{{< step >}}Writes flattened Avro schemas — all chunks expanded — to `outputs/avsc/`.{{< /step >}}
{{< step >}}Writes TypeScript type definitions to `outputs/typescript/`.{{< /step >}}
{{< step >}}Writes Protocol Buffer definitions to `outputs/proto/` and compiles them with `buf`.{{< /step >}}
{{< step >}}Assembles the three npm packages and bumps their versions.{{< /step >}}
{{< step >}}Writes the Markdown reference to `schemaList.md` and the schema library README.{{< /step >}}
{{< /steps >}}

### Useful shortcuts

```bash
npm run generate -- --help  # every option
npm run generate:check      # fail if the committed outputs are stale (CI)
npm run generate:dry-run    # show what would change, write nothing
npm run generate:types      # regenerate only TypeScript and Avro
npm run generate:proto      # regenerate only protobuf
npm run generate:packages   # proto, samples-lib, encoder, decoder
npm run generate:docs       # markdown + samples-lib
npm run schemas:list        # list the discovered schemas and chunks
npm run schemas:validate    # validate, and check every field is documented
npm run schemas:clean       # remove generated outputs
npm run verify              # typecheck + generate:check
```

## Generated outputs

| Format | Description | Location |
|---|---|---|
| **TypeScript** | Type definitions for every schema | `outputs/typescript/` |
| **Protocol Buffers** | `.proto` files for cross-language serialisation | `outputs/proto/` |
| **Avro** | Flattened schemas, all chunks expanded | `outputs/avsc/` |
| **Markdown** | Field-by-field reference | `schemaList.md` |

### npm packages

| Package | Contents |
|---|---|
| [`@observertc/schemas`](https://www.npmjs.com/package/@observertc/schemas) | Core TypeScript / JavaScript type definitions |
| [`@observertc/samples-encoder`](https://www.npmjs.com/package/@observertc/samples-encoder) | Binary encoding utilities |
| [`@observertc/samples-decoder`](https://www.npmjs.com/package/@observertc/samples-decoder) | Binary decoding utilities |

All three are versioned in lockstep with `sources/version.txt` by the generator.

## Project structure

```text
├── sources/                 # Source Avro schema definitions
│   ├── samples/             # Sample schemas (.avsc) and reusable chunks
│   ├── w3c/                 # W3C stats identifiers, copied into the library
│   └── version.txt          # Current schema version
├── src/                     # The generator (TypeScript)
├── outputs/                 # Generated outputs
│   ├── typescript/
│   ├── proto/
│   └── avsc/
├── npm-samples-lib/         # Generated core TypeScript library
├── npm-samples-encoder/     # Encoding utilities
├── npm-samples-decoder/     # Decoding utilities
├── CHANGELOG.md             # Schema change history
└── docs/GENERATOR.md        # How the generator works
```

## Adding a field

{{< steps >}}
{{< step >}}Edit the appropriate `.avsc` file in `sources/samples/`.{{< /step >}}
{{< step >}}**Document the field** — `npm run schemas:validate` fails if any field lacks a `doc`.{{< /step >}}
{{< step >}}Run `npm run generate` to regenerate all outputs.{{< /step >}}
{{< step >}}**Check the diff of `outputs/proto/`** before merging.{{< /step >}}
{{< step >}}Update `sources/version.txt` and add a `CHANGELOG.md` entry.{{< /step >}}
{{< /steps >}}

{{< callout context="caution" title="Protobuf field numbers are derived from field order" icon="alert-triangle" >}}
The generator sorts fields — repeated, then required, then optional, each group sorted by name —
and assigns protobuf numbers from that order.

**Inserting a field anywhere but the end of its group renumbers every field after it**, which
breaks the wire format for decoders built against the older schema. This is exactly what happened
in [3.3.0](../versions/v3-3-0/): adding `key` to `ClientIssue` moved `payload` from 2 → 3 and
`timestamp` from 3 → 4.

Always inspect the `outputs/proto/` diff.
{{< /callout >}}

### Schema guidelines

- Every field needs clear documentation.
- Use `null` unions for optional fields, with `"default": null`.
- camelCase field names.
- Add an `attachments` field for extensibility where appropriate.

## Versioning

Semantic versioning, with these conventions:

| Change type | Bump | Compatibility |
|---|---|---|
| Field addition | Minor | Additive — but check protobuf renumbering |
| Field removal | Major | Breaking |
| Type change | Major | Breaking |
| Documentation | Patch | Non-breaking |

- **PATCH** — library bugfixes and improvements
- **MINOR** — new fields and schema updates
- **MAJOR** — breaking changes to schema structure

The current version lives in `sources/version.txt` and is stamped into every generated artifact.

**Current: `3.3.0`.** See the [version history](../versions/) for the full 3.x record, or
[`CHANGELOG.md`](https://github.com/observertc/schemas/blob/master/CHANGELOG.md) for everything
back to 2.0.0.

### Compatibility model

- **Forward compatibility** — newer readers process older data.
- **Backward compatibility** — older readers may not see newer optional fields, and **will misread
  a record whose protobuf numbering shifted**.
- **Schema evolution** — new optional fields appended at the end of their group maintain
  compatibility.

### Migrating between versions

{{< steps >}}
{{< step >}}Review the [release page](../versions/) for every version you are skipping.{{< /step >}}
{{< step >}}Upgrade `@observertc/samples-encoder` and `@observertc/samples-decoder` together.{{< /step >}}
{{< step >}}Decode stored binary samples with a version matching what wrote them, or re-encode.{{< /step >}}
{{< step >}}Update processing for new fields you want to consume.{{< /step >}}
{{< step >}}Deploy incrementally and watch for decode errors before switching writers over.{{< /step >}}
{{< /steps >}}

## Publishing

The three npm packages are released by GitHub Actions using **npm trusted publishing (OIDC)** —
there is no `NPM_TOKEN`. Each package needs a Trusted Publisher registered once on npmjs.com
pointing at its workflow file; the exact settings are in
[`docs/GENERATOR.md`](https://github.com/observertc/schemas/blob/master/docs/GENERATOR.md#publishing).

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes in `sources/`.
4. Run `npm run generate`.
5. Run `npm run verify` and check the generated outputs.
6. Open a pull request.
