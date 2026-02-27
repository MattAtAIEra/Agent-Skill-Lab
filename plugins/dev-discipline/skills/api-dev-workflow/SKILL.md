---
name: api-dev-workflow
description: This skill should be used when the user asks to "build an API", "create a new endpoint", "add API functionality", or is about to start API development work. Enforces a spec-first discipline for API development to ensure quality and traceability.
version: 1.0.0
---

# API Development Workflow Discipline

API development must follow the process below. No step may be skipped. This discipline ensures every API endpoint has a complete spec, tests, and documentation.

## Workflow Steps

### 1. Write the API Spec (Spec First)

Before writing any code, draft a complete API specification in `doc/api-spec.md` (or the project's designated spec file):

- HTTP method and path
- Request body (fields, types, required/optional, defaults, descriptions)
- Response body (with example JSON)
- Error status codes and messages
- Authentication requirements
- Query parameters (if applicable)

Spec format example:

```markdown
### POST /api/resources

Create a resource.

**Request**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Y | Resource name |

**Response** `200`
{ "id": 1 }

**Error**
| Status Code | Message |
|-------------|---------|
| 400 | Missing required field |
```

### 2. Get User Confirmation

Present the spec to the user for review. Explicitly ask:

- Does the endpoint design meet the requirements?
- Are the field definitions complete?
- Does the error handling cover all scenarios?
- Is the authentication mechanism correct?

**Do not proceed to implementation without confirmation.**

### 3. Implement the API

Develop according to the confirmed spec:

- Create route files (follow the framework's file-based routing conventions)
- Implement request validation
- Implement business logic
- Implement error handling (per the error codes defined in the spec)
- Ensure the response format matches the spec

### 4. Write Tests

Write integration tests for each endpoint:

- Happy path (normal flow)
- Validation errors (missing required fields, format errors)
- Business logic errors (404, 409, etc.)
- Authentication tests (if applicable: no token, invalid token, expired token)

All tests must pass before proceeding to the next step.

### 5. Generate Postman Collection

Update or create a Postman Collection JSON:

- One request per endpoint
- Organize by module folders
- Include example request bodies
- Set environment variables (baseUrl, token, etc.)
- Use Postman Collection v2.1 format

### 6. Generate OpenAPI (Swagger)

Update or create an OpenAPI YAML:

- Use OpenAPI 3.0 format
- Define reusable schemas
- Include complete definitions for all endpoints
- Set security schemes (if applicable)

## Checklist

After completing each API, confirm the following:

- [ ] API spec written and confirmed by the user
- [ ] Code implementation complete
- [ ] Integration tests written and all passing
- [ ] Postman Collection updated
- [ ] OpenAPI Swagger updated
- [ ] Dev log entry recorded (using the `dev-log` skill)

## Common Violations

The following behaviors violate this discipline and must be avoided:

- Writing code before writing the spec
- Starting implementation without waiting for spec confirmation
- Skipping tests and jumping straight to documentation
- Only writing happy-path tests
- Generating Postman or Swagger for only some endpoints
- Failing to update specs and docs after API changes
