---
title: "Code Generation & Versioning"
description: "Generate type-safe language bindings and manage schema versions"
lead: "Code generation tools and version management for ObserveRTC schemas"
date: 2023-09-07T16:33:54+02:00
lastmod: 2023-09-07T16:33:54+02:00
draft: false
weight: 210
toc: true
---

## Code Generation

The ObserveRTC schema generator creates type-safe language bindings from Avro schema definitions.

**Repository**: [https://github.com/ObserveRTC/schemas](https://github.com/ObserveRTC/schemas)

### Generated Outputs

| Format | Description |
|--------|-------------|
| **TypeScript/JavaScript** | Type definitions and encoding/decoding utilities |
| **SQL Schemas** | BigQuery, PostgreSQL, Redshift, ClickHouse table definitions |
| **Protocol Buffers** | .proto files for cross-language serialization |
| **CSV Headers** | Column definitions for data export |
| **Avro Schema** | JSON schema definitions |

### NPM Packages

- `@observertc/schemas` - TypeScript type definitions
- `@observertc/samples-encoder` - Binary encoding utilities
- `@observertc/samples-decoder` - Binary decoding utilities

### Usage

```bash
git clone https://github.com/ObserveRTC/schemas.git
cd schemas
npm install
npm run compile
```

## Versioning

ObserveRTC schemas follow semantic versioning (SemVer) for compatibility management.

### Version Strategy

| Change Type | Version Bump | Compatibility |
|-------------|-------------|---------------|
| **Field addition** | Minor | Forward compatible |
| **Field removal** | Major | Breaking change |
| **Type change** | Major | Breaking change |
| **Documentation** | Patch | Non-breaking |

### Current Version

**Schema Version**: 3.0.0

### Migration

When upgrading between major versions:

1. Review breaking changes in release notes
2. Update type definitions
3. Modify data processing logic for removed/changed fields
4. Test with sample data
5. Deploy incrementally

### Compatibility

- **Forward compatibility**: Newer readers can process older data
- **Backward compatibility**: Older readers may not process newer optional fields
- **Schema evolution**: New optional fields maintain compatibility
