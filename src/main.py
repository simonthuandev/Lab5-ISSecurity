import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from core.output_handler import print_banner, print_section, print_info
from core.input_handler import prompt_menu, NavigateBack, NavigateMain, NavigateQuit
from core.menu_symmetric import symmetric_menu
from core.menu_asymmetric import asymmetric_menu
from core.menu_hash import hash_menu


def main():
    print_banner()
    print_info("Chào mừng bạn đến với Cryptography Toolkit!")
    print_info("Chương trình hỗ trợ: Mã hóa đối xứng, bất đối xứng và hàm băm.")

    while True:
        try:
            print_section("Menu Chính")
            options = {
                "1": "Mã hóa Đối xứng   — DES / 3DES / AES",
                "2": "Mã hóa Bất đối xứng — RSA",
                "3": "Hàm Băm            — MD5 / SHA-256",
            }
            choice = prompt_menu(
                options,
                "Chọn nhóm tính năng",
                back_label=None,
                main_label=None,
                quit_label="Thoát chương trình",
            )
        except (NavigateBack, NavigateMain):
            continue
        except NavigateQuit:
            print_info("Cảm ơn bạn đã sử dụng Cryptography Toolkit. Tạm biệt!")
            sys.exit(0)

        handler_map = {"1": symmetric_menu, "2": asymmetric_menu, "3": hash_menu}
        result = handler_map[choice]()

        if result == "Q":
            print_info("Cảm ơn bạn đã sử dụng Cryptography Toolkit. Tạm biệt!")
            sys.exit(0)


if __name__ == "__main__":
    main()
