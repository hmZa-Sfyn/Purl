def display_help():
    """Display help message with usage instructions."""
    help_text = """
\033[1mPurl Web Request Engine\033[0m
A CLI tool to send HTTP requests using a clean command syntax.

\033[1mUsage:\033[0m
  python3 purl.py <method> <url> [--payload <payload>] [--cookies <cookies>] [--headers <headers>]
  python3 purl.py <script.prl>
  python3 purl.py --help

\033[1mCommands:\033[0m
  get, post, put, delete, patch: Send an HTTP request with the specified method.
  <script.prl>                 : Run a script file containing a request.

\033[1mOptions:\033[0m
  --payload <data>  JSON or string payload for POST, PUT, PATCH requests.
  --cookies <data>  JSON or key=value pairs for cookies.
  --headers <data>  JSON key-value pairs for custom headers.
  --help            Show this help message.

\033[1mScript Format (.prl):\033[0m
  req-<method> <url>
  [/payload]
  <payload_data>
  [/cookies]
  <cookies_data>
  [/headers]
  <headers_data>

\033[1mExamples:\033[0m
  # Direct GET request
  python3 purl.py get https://api.example.com/data

  # POST request with JSON payload and cookies
  python3 purl.py post https://api.example.com/submit --payload '{"key": "value"}' --cookies '{"session": "abc123"}'

  # POST with form-data and key-value cookies
  python3 purl.py post https://api.example.com/submit --payload "name=John&age=30" --cookies "session=abc123"

  # Run a script file
  python3 purl.py script.prl

\033[1mScript Example (script.prl):\033[0m
  req-post https://api.example.com/submit
  /payload
  {"title": "foo", "body": "bar"}
  /cookies
  session=abc123
  /headers
  {"Authorization": "Bearer token123"}

\033[1mNotes:\033[0m
- Payloads can be JSON or raw strings.
- Cookies can be JSON or key=value pairs.
- Headers must be valid JSON.
- Responses are truncated at 1000 characters.
"""
    print(help_text)
