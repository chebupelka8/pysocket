import colorama

from typing import Tuple, Optional


class ServerNotifier:

    @staticmethod
    def notify_connected(address: Tuple[str, int]) -> None:
        print(colorama.Fore.GREEN + f"Client {address} connected." + colorama.Style.RESET_ALL)

    @staticmethod
    def notify_disconnected(address: Tuple[str, int]) -> None:
        print(colorama.Fore.RED + f"Client {address} disconnected." + colorama.Style.RESET_ALL)

    @staticmethod
    def start_server() -> None:
        print(colorama.Fore.LIGHTBLUE_EX + "Server started." + colorama.Style.RESET_ALL)

    @staticmethod
    def listening_server() -> None:
        print(colorama.Fore.LIGHTBLUE_EX + "Server listening..." + colorama.Style.RESET_ALL)


class ClientNotifier:

    @staticmethod
    def connection_notify(address: Tuple[str, int]) -> None:
        print(colorama.Fore.GREEN + f"Connected to {address}." + colorama.Style.RESET_ALL)

    @staticmethod
    def disconnection_notify(address: Tuple[str, int], reason: Optional[str] = None) -> None:
        print(colorama.Fore.RED + f"Disconnected from {address}." + colorama.Style.RESET_ALL)

        if reason is not None:
            print(colorama.Fore.RED + f"Reason: {reason}." + colorama.Style.RESET_ALL)
