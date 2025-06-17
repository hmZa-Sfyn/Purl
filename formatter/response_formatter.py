import json
import textwrap

def format_response(response):
    """Format the response for readable output."""
    if 'error' in response:
        return f"\033[31mError:\033[0m {response['error']}"
    
    output = [
        f"\033[32m✓ Request Successful\033[0m",
        f"Status: {response['status_code']}",
        f"URL: {response['url']}",
        "Headers:",
        json.dumps(response['headers'], indent=2)
    ]
    
    if response['json'] is not None:
        output.append("JSON Response:")
        output.append(json.dumps(response['json'], indent=2))
    else:
        output.append("Response Content:")
        content = response['content'][:1000]
        output.append(textwrap.indent(content, '  '))
        if len(response['content']) > 1000:
            output.append("  ... (content truncated)")
    
    return '\\n'.join(output)
