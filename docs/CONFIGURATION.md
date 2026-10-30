# Configuration

## Defaults

| Setting | Default | Meaning |
|---|---|---|
| Host | http://127.0.0.1:11434 | Ollama API address |
| Model | qwen2.5:3b | Model used for ghost text |
| Timeout | 30 seconds | Maximum wait for a model response |
| Temperature | 0.8 | Creativity level |
| Stream | on | Print text as it arrives |
| Color | on | Use ANSI colors when supported |

## Precedence

1. Command-line flags.
2. Environment variables.
3. Built-in defaults.

A flag always wins over an environment variable.

## Environment variables

```powershell
$env:GHOSTSHELL_HOST = "http://127.0.0.1:11434"
$env:GHOSTSHELL_MODEL = "qwen2.5:3b"
$env:GHOSTSHELL_TIMEOUT = "30"
$env:GHOSTSHELL_TEMPERATURE = "0.8"
$env:GHOSTSHELL_STREAM = "1"
$env:NO_COLOR = "1"
```

| Variable | Accepted values | Notes |
|---|---|---|
| GHOSTSHELL_HOST | A full http or https URL | No trailing slash required |
| GHOSTSHELL_MODEL | A model name installed in Ollama | Must not be empty |
| GHOSTSHELL_TIMEOUT | A positive number | Seconds |
| GHOSTSHELL_TEMPERATURE | A number from 0 to 2 | Higher is more random |
| GHOSTSHELL_STREAM | 1 or 0 | Also accepts true or false |
| NO_COLOR | Any non-empty value | Turns color off |

## Command-line flags

```powershell
python main.py --help
python main.py --model qwen2.5:0.5b
python main.py --host http://127.0.0.1:11434
python main.py --timeout 60
python main.py --temperature 0.6
python main.py --no-stream
python main.py --no-color
python main.py --check
```

| Flag | Effect |
|---|---|
| --model | Sets the model name |
| --host | Sets the Ollama API address |
| --timeout | Sets the request timeout in seconds |
| --temperature | Sets the model temperature |
| --no-stream | Waits for the full response before printing |
| --no-color | Turns color off |
| --check | Runs the health check and exits |
| --version | Prints the version and exits |

## Model selection

List installed models:

```powershell
ollama list
```

Download a model:

```powershell
ollama pull qwen2.5:3b
```

Use a different model for one session:

```powershell
python main.py --model llama3.2:3b
```

## Color

Color is on when the terminal appears to support it. The app also respects the NO_COLOR convention. Use --no-color when you capture output or when colors look wrong.

## Streaming

Streaming shows text as the model produces it. It feels faster. Use --no-stream when you want one clean block or when a terminal has trouble with partial lines.

## High-risk commands

High-risk commands are always blocked in the first release. There is no override flag. The model cannot approve a command. The app shows the reason for the block and returns to the prompt.

A typed-phrase override may be considered after the first release. It would still show the exact command and would still keep the model out of the decision.

## Configuration file

A local configuration file is planned but not part of the first release. Until then, use environment variables or flags. A future file will be read from the user profile, not from the repository, so local settings are never committed.

## Validation

Invalid values produce a clear message and a nonzero exit code. Examples:

- A timeout of zero or a negative number.
- A temperature outside 0 to 2.
- An empty model name.
- A host that is not an http or https URL.
