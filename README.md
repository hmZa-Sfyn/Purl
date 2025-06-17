# WebReqUtil: Purl

A CLI tool to send HTTP requests using a clean command syntax.

## Description

WebReqUtil is a command-line tool that allows you to send HTTP requests with various methods (GET, POST, PUT, DELETE, PATCH) and options such as payload, cookies, and headers. It supports both direct command-line usage and script files for more complex requests.

## Usage

```
python3 main.py <method> <url> [--payload <payload>] [--cookies <cookies>] [--headers <headers>]
python3 main.py <script.prl>
python3 main.py --help
```

### Commands:

-   `get`, `post`, `put`, `delete`, `patch`: Send an HTTP request with the specified method.
-   `<script.prl>`: Run a script file containing a request.

### Options:

-   `--payload <data>`: JSON or string payload for POST, PUT, PATCH requests.
-   `--cookies <data>`: JSON or key=value pairs for cookies.
-   `--headers <data>`: JSON key-value pairs for custom headers.
-   `--help`: Show this help message.

## Script Format (.prl):

```
req-<method> <url>
[/payload]
<payload_data>
[/cookies]
<cookies_data>
[/headers]
<headers_data>
```

## Examples:

### Direct GET request

```
python3 main.py get https://api.example.com/data
```

### POST request with JSON payload and cookies

```
python3 main.py post https://api.example.com/submit --payload '{"key": "value"}' --cookies '{"session": "abc123"}'
```

### POST with form-data and key-value cookies

```
python3 main.py post https://api.example.com/submit --payload "name=John&age=30" --cookies "session=abc123"
```

### Run a script file

```
python3 main.py script.prl
```

### Script Example (script.prl):

```
req-post https://api.example.com/submit
/payload
{"title": "foo", "body": "bar"}
/cookies
session=abc123
/headers
{"Authorization": "Bearer token123"}
```

## Project Structure

```
project/
├── main.py
├── examples/
│   ├── simple_get.prl
│   ├── get_with_query.prl
│   ├── post_json.prl
│   ├── post_form_data.prl
│   ├── put_update.prl
│   ├── patch_partial.prl
│   ├── delete_resource.prl
│   ├── get_with_cookies.prl
│   ├── post_with_all.prl
│   ├── put_raw_payload.prl
```

## Example Scripts

This project includes several example scripts in the `examples/` directory to demonstrate various HTTP methods and options.

### Simple GET Request

`examples/simple_get.prl`: Fetches a list of posts using a basic GET request.

Usage:

```
python3 main.py examples/simple_get.prl
```

### GET with Query Parameters

`examples/get_with_query.prl`: Fetches a specific post by ID using query parameters.

Usage:

```
python3 main.py examples/get_with_query.prl
```

### POST with JSON Payload

`examples/post_json.prl`: Creates a new post with a JSON payload and custom headers.

Usage:

```
python3 main.py examples/post_json.prl
```

### POST with Form Data

`examples/post_form_data.prl`: Submits a post using form-data and key-value cookies.

Usage:

```
python3 main.py examples/post_form_data.prl
```

### PUT to Update Resource

`examples/put_update.prl`: Updates an existing post with a complete JSON payload.

Usage:

```
python3 main.py examples/put_update.prl
```

### PATCH for Partial Update

`examples/patch_partial.prl`: Partially updates a post’s title using PATCH.

Usage:

```
python3 main.py examples/patch_partial.prl
```

### DELETE Resource

`examples/delete_resource.prl`: Deletes a post with an authorization header.

Usage:

```
python3 main.py examples/delete_resource.prl
```

### GET with JSON Cookies

`examples/get_with_cookies.prl`: Fetches users with JSON-formatted cookies.

Usage:

```
python3 main.py examples/get_with_cookies.prl
```

### POST with All Options

`examples/post_with_all.prl`: Demonstrates a POST request using payload, cookies, and headers.

Usage:

```
python3 main.py examples/post_with_all.prl
```

### PUT with Raw Payload

`examples/put_raw_payload.prl`: Updates a post using a raw string payload and JSON cookies.

Usage:

```
python3 main.py examples/put_raw_payload.prl
```

## Notes:

-   Payloads can be JSON or raw strings.
-   Cookies can be JSON or key=value pairs.
-   Headers must be valid JSON.
-   Responses are truncated at 1000 characters.
