# Copilot Commit Message Instructions

1. **Commit Message Structure:**
    - Use the following format:
      ```
      <type>(file relative path): <short summary>

      <detailed description, if necessary>
      ```
    - Example:
      ```
      feat(api/orders.py): add endpoint for creating new orders

      Implements POST /orders with validation and error handling.
      ```

2. **Types:**
    - `feat`: New feature
    - `fix`: Bug fix
    - `docs`: Documentation changes
    - `refactor`: Code refactoring (no feature or fix)
    - `test`: Adding or updating tests
    - `chore`: Maintenance tasks (dependencies, configs)
    - `ci`: CI/CD related changes

3. **Paths:**
    - Use relative path if the change affects a specific file or directory.
    - Use three dots `...` instead of relative paths for changes affecting two or more staged files.

4. **Staged Changes:**
   - Consider only the changes staged for commit.

## Examples

- `fix(backend/models.py): correct typo in Product model`
- `feat(backend/api.py): implement GET /flowers endpoint`
- `docs(backend/readme.md): update setup instructions`
- `test(backend/api.py): add tests for order creation`
- `chore(frontend/package.json): update dependencies`
