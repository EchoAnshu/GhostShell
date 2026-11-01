# Technology Stack — GhostShell

## 1. Core stack

| Layer | Technology | Role |
|---|---|---|
| Programming language | Python 3.10+ | Application logic |
| Local inference runtime | Ollama | Runs the model locally |
| Initial model | Qwen2.5 3B | Generates commentary and explanations |
| Model interface | Ollama HTTP API | Connects Python to local inference |
| Initial shell | Windows PowerShell | Command-line environment |
| Terminal styling | ANSI escape codes | Colored and formatted output |
| Testing | Python `unittest` or `pytest` | Verify core behavior |

## 2. Why this stack?

### Python
Simple to read, quick to prototype, and suitable for HTTP requests and command-line applications.

### Ollama
Provides a straightforward local interface for downloading and running open-weight models.

### Qwen2.5 3B
A relatively small model to start experimenting with on a consumer laptop. Actual speed and memory use depend on quantization and hardware.

### PowerShell
Matches the initial Windows development environment. Shell-specific behavior should be isolated so other shells can be supported later.

## 3. Dependencies

Keep runtime dependencies minimal. The initial Python application can use:

- `requests` for HTTP requests to Ollama.
- Python standard-library modules for subprocess execution, input handling, and terminal formatting.

Add packages only when a concrete feature needs them.

## 4. Configuration

The following should eventually be configurable:

- Ollama host URL
- Model name
- Response temperature
- Request timeout
- Ghost personality / response style

## 5. Model flexibility

Ollama supports multiple models. GhostShell should read the model name from configuration or an environment variable so users can switch models without changing application logic.

Before distributing a model or bundling it with the project, check its license and redistribution terms.
