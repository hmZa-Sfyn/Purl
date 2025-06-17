def format_error(error, command):
    """Format errors with line numbers and context, inspired by Vite/Nushell."""
    lines = command.strip().split('\\n')
    error_title = "\\033[1;31mRequest Error\\033[0m"  # Bold red
    border_line = "━" * (len(error_title) + 4)  # +4 for padding
    
    output = [
        f"\\033[31m{border_line}\\033[0m",
        f"\\033[31m┃ \\033[0m{error_title}\\033[31m ┃\\033[0m",
        f"\\033[31m{border_line}\\033[0m",
        f"\\033[1;31mMessage:\\033[0m {error.message}",  # Bold red
    ]
    
    if error.file_name:
        output.append(f"\\033[1;31mFile:\\033[0m {error.file_name}")  # Bold red
    
    if error.line_number is not None and error.context:
        output.append("\\033[1;31mLocation:\\033[0m")  # Bold red
        start_line = max(0, error.line_number - 2)
        end_line = min(len(lines), error.line_number + 1)
        for i in range(start_line, end_line):
            line_num = i + 1
            prefix = "➤" if line_num == error.line_number else " "
            line = lines[i]
            output.append(f"{prefix} \\033[34m{line_num:3d}\\033[0m | {line}")  # Blue line number
            if line_num == error.line_number:
                error_column = 0
                if error.context and error.context in line:
                    error_column = line.index(error.context)
                arrow_line = " " * (5 + error_column) + "\\033[31m" + "^" * (len(error.context) if error.context else 1) + "\\033[0m"  # Red arrow
                output.append(arrow_line)
    
    output.append("\\033[1;33mHint:\\033[0m Ensure the command follows the correct syntax:")  # Bold yellow
    output.append("  req-<method> <url>")
    output.append("  [/payload]")
    output.append("  <payload_data>")
    output.append("  [/cookies]")
    output.append("  <cookies_data>")
    output.append("  [/headers]")
    output.append("  <headers_data>")
    output.append(f"\\033[31m{border_line}\\033[0m")
    return "\\n".join(output)
