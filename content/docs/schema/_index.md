---
title: "Schema"
description: "ObserveRTC Schema Package"
lead: "Strongly typed, versioned schema for monitoring data"
date: 2023-09-07T16:33:54+02:00
lastmod: 2023-09-07T16:33:54+02:00
draft: false
weight: 200
toc: true
---

## Overview

The ObserveRTC Schema package provides a strongly typed, versioned schema system for collected monitoring data. It ensures interoperability and consistency between all ObserveRTC components while supporting forward compatibility for evolving metrics and requirements.

## Key Features

### Strongly Typed Schema
- **Type safety** - Comprehensive TypeScript definitions for all data structures
- **Compile-time validation** - Catch schema mismatches during development
- **IDE support** - Full IntelliSense and autocomplete for schema fields
- **Runtime validation** - Optional runtime type checking for production environments

### Version Management
- **Semantic versioning** - Clear versioning strategy for schema evolution
- **Forward compatibility** - Newer components can work with older schema versions
- **Backward compatibility** - Legacy data remains accessible with schema upgrades
- **Migration support** - Automated migration tools between schema versions

### Interoperability
- **Component consistency** - All ObserveRTC libraries use the same schema definitions
- **Cross-platform support** - Schema available for JavaScript, TypeScript, and other languages
- **Standardized formats** - JSON Schema and Protocol Buffer definitions
- **Validation tools** - Built-in validators for data integrity

## Installation

```bash
npm install @observertc/schemas
```

## Quick Start

### TypeScript Integration

```typescript
import {
  ClientSample,
  SfuSample,
  ObserverEventReport
} from '@observertc/schemas';

// Type-safe sample creation
const clientSample: ClientSample = {
  timestamp: Date.now(),
  clientId: 'client-123',
  type: 'outbound-rtp',
  data: {
    ssrc: 12345,
    bytesSent: 1024,
    packetsSent: 100
  }
};

// Validate sample structure
import { validateClientSample } from '@observertc/schemas/validators';

const isValid = validateClientSample(clientSample);
if (!isValid) {
  console.error('Invalid client sample structure');
}
```

### JavaScript Usage

```javascript
import { schemas, validators } from '@observertc/schemas';

// Access schema definitions
const clientSampleSchema = schemas.ClientSample;

// Validate data against schema
const sample = {
  timestamp: Date.now(),
  clientId: 'client-123'
  // ... sample data
};

if (validators.validateClientSample(sample)) {
  console.log('Sample is valid');
} else {
  console.error('Sample validation failed');
}
```

## Documentation Sections

Explore the detailed documentation for different aspects of the Schema package:

### [Code Generation & Versioning](./general)
Learn about generating type-safe language bindings, managing schema versions, and the development workflow.

### [ClientSample Types](./clientsample)
Complete reference for ClientSample schema structure, field definitions, and all available statistics types.
