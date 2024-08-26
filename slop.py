from colorama import Fore
import random
import requests
import threading
import json


def load_proxies(file_path):
    with open(file_path, "r") as file:
        proxies = [line.strip() for line in file]
    return proxies


def save_account_info(username, token, user_code, file_path="acc_info.txt"):
    with open(file_path, "a") as file:
        file.write(f"{username} | {token} | {user_code}\n")


def tryRegister(proxies):
    url = "https://app.bunkrr.su/api/register"
    data = {
        "username": "lawyer_" + str(random.randint(100000, 999999)),
        "password": "jeremyfragrance",
        "invitation_code": "",
    }

    proxy = random.choice(proxies)
    proxies_dict = {"http": proxy, "https": proxy}

    try:
        response = requests.post(
            url, json=data, proxies=proxies_dict, allow_redirects=True, timeout=10
        )
        print(
            f'[{Fore.YELLOW}?{Fore.RESET}] {response.status_code} | Attempting to create account: {data["username"]}'
        )
        response_json = response.json()
        if response.status_code == 429:
            print(
                f"[{Fore.RED}-{Fore.RESET}] {response.status_code} | Rate limited, retrying with new proxy..."
            )
            return tryRegister(proxies)
        if "token" in response_json:
            token = response_json["token"]
            user_code = response_json.get("user_code")
            save_account_info(data["username"], token, user_code)
            print(
                f'[{Fore.GREEN}+{Fore.RESET}] {response.status_code} | Successfully created account: {data["username"]}'
            )
    except Exception as e:
        with open("errors.txt", "a") as file:
            file.write(f"{str(e)}\n")


def main():
    proxies = load_proxies("proxies.txt")
    threadc = 4
    threads = []
    for _ in range(threadc):
        thread = threading.Thread(target=tryRegister, args=(proxies,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
