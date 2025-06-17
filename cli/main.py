import argparse
import sys
from core import parse_request, execute_request, RequestError
from formatter import format_response, format_error

def main():
    """Main function to run the CLI app."""
    parser = argparse.ArgumentParser(
        description="Purl Web Request Engine",
        add_help=False
    )
    parser.add_argument('command', help="HTTP method (get, post, put, delete, patch) or script file")
    parser.add_argument('url', nargs='?', help="Target URL for the request")
    parser.add_argument('--payload', help="Payload data (JSON or string)")
    parser.add_argument('--cookies', help="Cookies (JSON or key=value pairs)")
    parser.add_argument('--headers', help="Headers (JSON)")
    parser.add_argument('--help', action='store_true', help="Show help message")
    
    args = parser.parse_args()
    
    if args.help:
        display_help()
        sys.exit(0)
    
    if not args.command:
        print("\\033[31mError: Command or script file required.\\033[0m")
        display_help()
        sys.exit(1)
    
    try:
        # Check if command is a script file
        if args.command.endswith('.prl'):
            try:
                with open(args.command, 'r', encoding='utf-8') as f:
                    command = f.read()
            except UnicodeDecodeError:
                print(f"\\033[31mError: Script file '{{args.command}}' contains invalid UTF-8 encoding.\\033[0m")
                sys.exit(1)
            file_name = args.command
            request = parse_request(command, file_name)
        else:
            # Validate method
            if args.command.lower() not in ['get', 'post', 'put', 'delete', 'patch']:
                raise RequestError(
                    f"Invalid method '{{args.command}}'. Use get, post, put, delete, or patch.",
                    context=args.command
                )
            
            if not args.url:
                raise RequestError(
                    "URL is required for direct requests.",
                    context=""
                )
            
            # Construct command in script format
            command_lines = [f"req-{{args.command}} {{args.url}}"]
            if args.payload:
                command_lines.extend(["/payload", args.payload])
            if args.cookies:
                command_lines.extend(["/cookies", args.cookies])
            if args.headers:
                command_lines.extend(["/headers", args.headers])
            command = '\\n'.join(command_lines)
            file_name = None
            request = parse_request(command)
        
        response = execute_request(request)
        print("\\033[1mResponse:\\033[0m")
        print(format_response(response))
    
    except RequestError as e:
        error_command = command if command else (f"req-{{args.command}} {{args.url}}" if args.command and args.url else args.command or "")
        print(format_error(e, error_command))
        sys.exit(1)
    except FileNotFoundError:
        print(f"\\033[31mError: Script file '{{args.command}}' not found.\\033[0m")
        sys.exit(1)
    except Exception as e:
        print(f"\\033[31mUnexpected error:\\033[0m {{str(e)}}")
        sys.exit(1)

if __name__ == "__main__":
    main()
