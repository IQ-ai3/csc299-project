def main():
    """Package entrypoint: call the main function from src/main.py"""
    # Import here to keep module lightweight until entrypoint is used
    from .main import main as _main
    return _main()

if __name__ == '__main__':
    main()
