from cli import handle_command

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [arguments]")
        return
    command = sys.argv[1]
    args = sys.argv[2:]
    handle_command(command, args)

if __name__ == "__main__":
    main()