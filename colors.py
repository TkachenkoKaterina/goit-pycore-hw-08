from colorama import Fore, Back, Style, init

# Initialize Colorama
init(autoreset=True)

# Color utilities
def green(text):
    return Fore.GREEN + text + Style.RESET_ALL

def greeting(*texts):
    # Convert all texts to a single string separated by commas
    if isinstance(texts[0], list):
        texts = texts[0]  # Unpack the list if it's the first argument
    return ', '.join(green(text) for text in texts)

def helper(text):
    return Fore.BLUE + text + Style.RESET_ALL

def success(text):
    return Fore.WHITE + Back.GREEN + text + Style.RESET_ALL

def warning(text):
    return Fore.WHITE + Back.YELLOW + text + Style.RESET_ALL

def danger(text):
    return Fore.WHITE + Back.RED + text + Style.RESET_ALL

