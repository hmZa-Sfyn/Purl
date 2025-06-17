import re
import json
from core.request_error import RequestError

def parse_request(command, file_name=None):
    """Parse the input command string into a structured request object."""
    lines = command.strip().split('\n')
    request = {
        'method': None,
        'url': None,
        'payload': None,
        'cookies': None,
        'headers': None
    }
    
    # Parse first line for method and URL
    first_line = lines[0].strip()
    method_match = re.match(r'^req-(get|post|put|delete|patch)\s+(.+)$', first_line, re.IGNORECASE)
    if not method_match:
        raise RequestError(
            "Invalid request command. Use 'req-<method> <url>' where method is get, post, put, delete, or patch.",
            line_number=1,
            context=first_line,
            file_name=file_name
        )
    
    request['method'] = method_match.group(1).upper()
    request['url'] = method_match.group(2).strip()
    
    # Validate URL
    if not re.match(r'^https?://', request['url'], re.IGNORECASE):
        raise RequestError(
            f"Invalid URL: '{request['url']}'. URL must start with http:// or https://.",
            line_number=1,
            context=first_line,
            file_name=file_name
        )
    
    # Parse sections: payload, cookies, headers
    i = 1
    current_section = None
    section_lines = []
    
    while i < len(lines):
        line = lines[i].strip()
        if line in ['/payload', '/cookies', '/headers']:
            if current_section and section_lines:
                content = '\\n'.join(section_lines).strip()
                try:
                    if content:
                        if current_section == 'payload':
                            request['payload'] = json.loads(content) if content else None
                        elif current_section == 'cookies':
                            request['cookies'] = json.loads(content)
                        elif current_section == 'headers':
                            request['headers'] = json.loads(content)
                    else:
                        request[current_section] = None
                except json.JSONDecodeError as e:
                    if current_section == 'payload':
                        request['payload'] = content
                    elif current_section == 'cookies':
                        cookies = {}
                        for idx, cookie_line in enumerate(section_lines):
                            if '=' in cookie_line:
                                key, value = cookie_line.split('=', 1)
                                cookies[key.strip()] = value.strip()
                            else:
                                raise RequestError(
                                    f"Invalid cookie format: '{cookie_line}'. Use 'key=value' or JSON.",
                                    line_number=i - len(section_lines) + idx + 1,
                                    context=cookie_line,
                                    file_name=file_name
                                )
                        request['cookies'] = cookies if cookies else None
                    elif current_section == 'headers':
                        raise RequestError(
                            f"Invalid headers format: '{content}'. Headers must be valid JSON.",
                            line_number=i - len(section_lines) + 1,
                            context=content,
                            file_name=file_name
                        )
            current_section = line[1:]
            section_lines = []
        else:
            section_lines.append(line)
        i += 1
    
    # Process the last section
    if current_section and section_lines:
        content = '\\n'.join(section_lines).strip()
        try:
            if content:
                if current_section == 'payload':
                    request['payload'] = json.loads(content) if content else None
                elif current_section == 'cookies':
                    request['cookies'] = json.loads(content)
                elif current_section == 'headers':
                    request['headers'] = json.loads(content)
            else:
                request[current_section] = None
        except json.JSONDecodeError as e:
            if current_section == 'payload':
                request['payload'] = content
            elif current_section == 'cookies':
                cookies = {}
                for idx, cookie_line in enumerate(section_lines):
                    if '=' in cookie_line:
                        key, value = cookie_line.split('=', 1)
                        cookies[key.strip()] = value.strip()
                    else:
                        raise RequestError(
                            f"Invalid cookie format: '{cookie_line}'. Use 'key=value' or JSON.",
                            line_number=i - len(section_lines) + idx + 1,
                            context=cookie_line,
                            file_name=file_name
                        )
                request['cookies'] = cookies if cookies else None
            elif current_section == 'headers':
                raise RequestError(
                    f"Invalid headers format: '{content}'. Headers must be valid JSON.",
                    line_number=i - len(section_lines) + 1,
                    context=content,
                    file_name=file_name
                )
    
    return request
