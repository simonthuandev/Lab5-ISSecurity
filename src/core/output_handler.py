import subprocess
import sys


# ── ANSI Colors ───────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"
MAGENTA= "\033[95m"
DIM    = "\033[2m"


def print_banner():
    banner = f"""
{CYAN}{BOLD}
╔══════════════════════════════════════════════════╗
║          🔐  CRYPTOGRAPHY TOOLKIT  🔐            ║
╚══════════════════════════════════════════════════╝
{RESET}"""
    print(banner)


def print_section(title: str):
    width = 52
    print(f"\n{BLUE}{BOLD}{'─' * width}")
    print(f"  {title}")
    print(f"{'─' * width}{RESET}")


def print_success(message: str):
    print(f"{GREEN}{BOLD}✔  {message}{RESET}")


def print_error(message: str):
    print(f"{RED}{BOLD}✖  Lỗi: {message}{RESET}")


def print_warning(message: str):
    print(f"{YELLOW}⚠  {message}{RESET}")


def print_info(message: str):
    print(f"{CYAN}ℹ  {message}{RESET}")


def print_result_box(label: str, value: str):
    """Hiển thị kết quả trong khung đẹp."""
    width = 60
    print(f"\n{GREEN}{BOLD}┌{'─' * width}┐")
    print(f"│  {label:<{width - 2}}│")
    print(f"├{'─' * width}┤{RESET}")
    # Wrap value if too long
    for i in range(0, max(1, len(value)), width - 4):
        chunk = value[i : i + width - 4]
        print(f"{GREEN}│  {chunk:<{width - 2}}│{RESET}")
    print(f"{GREEN}{BOLD}└{'─' * width}┘{RESET}")


def print_key_box(label: str, value: str):
    """Hiển thị khóa/key trong khung."""
    width = 60
    print(f"\n{YELLOW}{BOLD}┌{'─' * width}┐")
    print(f"│  {label:<{width - 2}}│")
    print(f"├{'─' * width}┤{RESET}")
    lines = value.strip().splitlines()
    for line in lines:
        for i in range(0, max(1, len(line)), width - 4):
            chunk = line[i : i + width - 4]
            print(f"{YELLOW}│  {chunk:<{width - 2}}│{RESET}")
    print(f"{YELLOW}{BOLD}└{'─' * width}┘{RESET}")


def show_result_actions(result_text: str):
    """Hiển thị tuỳ chọn sau khi có kết quả: Thử lại / Menu."""
    print(f"\n{DIM}{'─' * 54}{RESET}")
    print(f"{BOLD}Tùy chọn:{RESET}")
    print(f"  {CYAN}[R]{RESET} Thử lại (quay về chức năng hiện tại)")
    print(f"  {CYAN}[M]{RESET} Quay về Menu chính")
    print(f"  {CYAN}[Q]{RESET} Thoát chương trình")
    print(f"{DIM}{'─' * 54}{RESET}")

    while True:
        choice = input(f"\n{BOLD}Chọn [{CYAN}R/M/Q{RESET}{BOLD}]: {RESET}").strip().upper()
        if choice in ("R", "M", "Q"):
            return choice
        else:
            print_warning("Vui lòng nhập R, M hoặc Q.")
