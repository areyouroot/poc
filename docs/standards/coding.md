<!-- 
Author: Antigravity
Purpose: Defines the universal coding standards, naming conventions, and language-specific best practices for the project.
-->
# Coding Standards

This document outlines the coding standards and best practices for this project. Adhering to these standards ensures code readability, maintainability, and scalability.

## 0. Documentation Standards
All documentation files and source files MUST start with a header containing the author and the purpose of the file.

```markdown
<!-- 
Author: [Name]
Purpose: [Brief description of what this file contains/does]
-->
```

## 1. Naming Conventions (Universal)
To maintain consistency across languages, the following naming conventions are enforced:
- **Variables:** Use **PascalCase** (e.g., `UserName`, `IsActive`).
- **Classes:** Use **PascalCase** (e.g., `UserManager`).
- **Functions / Methods:** Use **PascalCase** (e.g., `CalculateTotal`, `GetData`).

## 2. Core Principles
- **SOLID Principles:** Follow Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion.
- **DRY (Don't Repeat Yourself):** Avoid logic duplication. Use modular functions and shared utilities.
- **KISS (Keep It Simple, Stupid):** Prefer simple, readable code over clever or complex solutions.
- **YAGNI (You Ain't Gonna Need It):** Do not implement features until they are actually needed.

## 3. C# Standards
- **Regions:** Use `#region` and `#endregion` to group related blocks of code (e.g., Private Fields, Public Properties, Methods).
- **Namespaces:** Use File-scoped namespaces (e.g., `namespace MyProject.Services;`) to reduce nesting.
- **Async Suffix:** All asynchronous methods must end with the `Async` suffix (e.g., `SaveDataAsync`).
- **Type Inference:** Use `var` for local variables when the type is obvious from the right-hand side.
- **LINQ:** Prefer LINQ queries for data manipulation for better readability.
- **Private Fields:** Use camelCase with an underscore prefix (e.g., `_databaseConnection`).

## 4. JavaScript / TypeScript Standards
- **Type Safety:** 
    - Avoid the `any` type at all costs; use `unknown` if the type is truly dynamic.
    - Prefer `interface` for public APIs and `type` for unions or aliases.
- **Readonly:** Use the `readonly` modifier for properties that should not be modified after initialization.
- **Null Safety:** Use Optional Chaining (`?.`) and Nullish Coalescing (`??`) instead of manual null checks.
- **Variables:** Use `const` by default. Use `let` only if the value changes. Never use `var`.
- **Async/Await:** Avoid raw Promises; use `async/await` for all asynchronous logic.

## 5. Python Standards
- **PEP 8:** Follow the official Python style guide for naming conventions and layout.
- **Type Hinting:** Use type hints (e.g., `def func(a: int) -> str:`) for all function signatures.
- **Tooling:** Use **Ruff** for extremely fast linting and formatting.
- **Data Validation:** Use **Pydantic** models for parsing and validating external data.

## 6. Security & Environment
- **Secrets:** NEVER hardcode API keys, passwords, or secrets.
- **Configuration:** Use `.env` files and environment variables for configuration.
- **Input Validation:** Always sanitize and validate user input to prevent injection attacks.

## 7. Copilot & AI Guidelines
Every function added by Copilot MUST include the following header to track ownership and intent.

```javascript
//abdul faheem
//<summary>
// <detailed description of the code and its purpose>
//</summary>
```

### Example:
```javascript
//abdul faheem
//<summary>
// This function calculates the sum of two numbers.
//</summary>
function Add(NumberA, NumberB) {
    return NumberA + NumberB;
}
```
