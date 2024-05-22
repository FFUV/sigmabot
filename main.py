from importlib.metadata import requires
import websocket
import ssl
import requests
from json import loads, dumps
import random
import time
from datetime import datetime
import socket

nick = 'SigmaBOT#9382LK'  # change this to your bot name!!!
ws = websocket.create_connection("wss://hack.chat/chat-ws", sslopt={"cert_reqs": ssl.CERT_NONE})  # 1: connect
ws.send(dumps({'cmd': 'join', 'channel': 'programming', 'nick': nick, 'pass': '<your password>'}))  # 2: join # change bot to the channel you want it to join and change its pass to a good password
print('The bot is now running...')

class GlobalVars:
    def __init__(self):
        self.userinfo = {}
        self.users = []
        self.afk_users = {}
        self.scramble_word = None
        self.scramble_start_time = None
        self.bank = {}
        self.messages = {}
        self.inventory = {}
        self.scramble_words = ["example", "scramble", "words", "for", "bot", "code", "development"]

def get_json(url):
    x = requests.get(url)
    return x.json()

vars = GlobalVars()

def get_weather(location):
    # Placeholder for weather API call
    return f"Weather for {location}: Sunny, 25°C"

def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_definition(word):
    # Placeholder for dictionary API call
    return f"Definition of {word}: A sample definition."

def coinflip():
    return "Heads" if random.randint(0, 1) == 0 else "Tails"

def diceroll():
    return str(random.randint(1, 6))

def get_geoip(ip):
    # Placeholder for GeoIP API call
    return f"GeoIP for {ip}: Sample Address"

def get_quote():
    json_data = get_json('https://api.quotable.io/random')
    return f'"{json_data["content"]}" - {json_data["author"]}'

def translate_text(text, to_lang='en'):
    # Placeholder for translation API call
    return f"Translated text to {to_lang}: {text}"

def resolve_dns(domain):
    try:
        ip = socket.gethostbyname(domain)
        return f'DNS for {domain}: {ip}'
    except socket.gaierror:
        return f'Unable to resolve DNS for {domain}'

def scramble_word():
    word = random.choice(vars.scramble_words)
    scrambled = ''.join(random.sample(word, len(word)))
    vars.scramble_word = word
    vars.scramble_start_time = time.time()
    return scrambled

def evaluate_code(language, code):
    # Placeholder for code evaluation (real implementation would require a backend service)
    return f"Output of {language} code: {code}"

def shorten_url(url):
    # Placeholder for URL shortening service
    return f"Shortened URL for {url}: short.ly/{random.randint(1000,9999)}"

def search_urbandict(term):
    # Placeholder for Urban Dictionary API call
    return f"Urban Dictionary for {term}: Sample definition and example."

def search_ddg(query):
    # Placeholder for DuckDuckGo search
    return f"Top search result for {query} on DDG: https://ddg.gg/?q={query.replace(' ', '+')}"

def solve_math(expression):
    # Placeholder for math solving and explanation
    return f"Solved {expression}: {eval(expression)} (example explanation)"

def add_to_inventory(user, item):
    if user not in vars.inventory:
        vars.inventory[user] = []
    vars.inventory[user].append(item)
    return f"Congratulations on your purchase, {user}! You bought {item}."

def handle_command(result):
    msg = result['text']
    user = result['nick']
    if msg == 'hello':
        ws.send(dumps({'cmd': 'chat', 'text': 'Erm.... what the sigma!'}))  # change this to your custom hello message
    elif msg.startswith('%'):
        cmdlist = msg.split(' ')
        cmdname = cmdlist[0][1:]
        sendmsg = ''
        if cmdname == 'help':
            if len(cmdlist) == 1:
                sendmsg = (f"@{user} - Available commands:\n"
                           "help, list, cookie, pie, shoot, hug, weather, time, dict, urbdict, math, dns, geoip, torcheck, shorten, coinflip, diceroll, quote, scramble, translate, afk, tripmsg, nick2trips, trip2nicks, wa, ddg, newnym, get, cgpt, oreo, clearc, eval, aliases, autokick, trustlist, bank, topbank, shop, inventory.\n"
                           "Run %help <command> for more information about a specific command.\n"
                           "This bot is operated by SigmaBOT. To report any bugs, email muusyinc@gmail.com")
            else:
                sendmsg = f"Help for {cmdlist[1]}: Detailed information about {cmdlist[1]} command."
        elif cmdname == 'weather':
            if len(cmdlist) >= 2:
                location = ' '.join(cmdlist[1:])
                sendmsg = get_weather(location)
            else:
                sendmsg = 'Please provide a location for the weather command.'
        elif cmdname == 'time':
            sendmsg = get_time()
        elif cmdname == 'dict':
            if len(cmdlist) >= 2:
                word = cmdlist[1]
                sendmsg = get_definition(word)
            else:
                sendmsg = 'Please provide a word to define.'
        elif cmdname == 'coinflip':
            sendmsg = coinflip()
        elif cmdname == 'diceroll':
            sendmsg = diceroll()
        elif cmdname == 'geoip':
            if len(cmdlist) >= 2:
                ip = cmdlist[1]
                sendmsg = get_geoip(ip)
            else:
                sendmsg = 'Please provide an IP address.'
        elif cmdname == 'quote':
            sendmsg = get_quote()
        elif cmdname == 'translate':
            if len(cmdlist) >= 2:
                text = ' '.join(cmdlist[1:])
                sendmsg = translate_text(text)
            else:
                sendmsg = 'Please provide text to translate.'
        elif cmdname == 'scramble':
            sendmsg = f"Unscramble this word: {scramble_word()}"
        elif cmdname == 'afk':
            reason = ' '.join(cmdlist[1:]) if len(cmdlist) > 1 else 'No reason provided'
            vars.afk_users[user] = reason
            sendmsg = f"{user} has been marked as AFK. Reason: {reason}"
        elif cmdname == 'nick2trips':
            if len(cmdlist) >= 2:
                target_nick = cmdlist[1]
                if target_nick in vars.userinfo:
                    sendmsg = f"{target_nick}'s trip: {vars.userinfo[target_nick]['trip']}"
                else:
                    sendmsg = f"User {target_nick} not found."
            else:
                sendmsg = 'Please provide a nickname.'
        elif cmdname == 'trip2nicks':
            if len(cmdlist) >= 2:
                target_trip = cmdlist[1]
                found_nicks = [nick for nick, info in vars.userinfo.items() if info['trip'] == target_trip]
                if found_nicks:
                    sendmsg = f"Nicks for trip {target_trip}: {', '.join(found_nicks)}"
                else:
                    sendmsg = f"No users found with trip {target_trip}."
            else:
                sendmsg = 'Please provide a trip.'
        elif cmdname == 'pie':
            if len(cmdlist) == 1:
                sendmsg = f"/me {user} has eaten a pie!"
            else:
                recipient = ' '.join(cmdlist[1:])
                sendmsg = f"/me {user} has given {recipient} a pie!"
        elif cmdname == 'cookie':
            if len(cmdlist) == 1:
                sendmsg = f"/me {user} has eaten a cookie!"
            else:
                recipient = ' '.join(cmdlist[1:])
                sendmsg = f"/me {user} has given {recipient} a cookie!"
        elif cmdname == 'hug':
            if len(cmdlist) == 1:
                sendmsg = f"/me {user} has given themselves a hug!"
            else:
                recipient = ' '.join(cmdlist[1:])
                sendmsg = f"/me {user} has hugged {recipient}!"
        elif cmdname == 'list':
            sendmsg = f"Users in the chatroom: {', '.join(vars.users)}"
        elif cmdname == 'dns':
            if len(cmdlist) >= 2:
                domain = cmdlist[1]
                sendmsg = resolve_dns(domain)
            else:
                sendmsg = 'Please provide a domain to resolve.'
        elif cmdname == 'eval':
            if len(cmdlist) >= 3:
                language = cmdlist[1]
                code = ' '.join(cmdlist[2:])
                sendmsg = evaluate_code(language, code)
            else:
                sendmsg = 'Please provide a language and code to evaluate.'
        elif cmdname == 'shorten':
            if len(cmdlist) >= 2:
                url = cmdlist[1]
                sendmsg = shorten_url(url)
            else:
                sendmsg = 'Please provide a URL to shorten.'
        elif cmdname == 'bank':
            balance = vars.bank.get(user, 0)
            sendmsg = f"{user}'s bank balance: {balance} points"
        elif cmdname == 'topbank':
            sorted_bank = sorted(vars.bank.items(), key=lambda item: item[1], reverse=True)
            top_users = [f"{u}: {b} points" for u, b in sorted_bank[:5]]
            sendmsg = f"Top bank balances:\n" + "\n".join(top_users)
        elif cmdname == 'shop':
            sendmsg = ("Shop:\n"
                       "10 points = bamboo\n"
                       "100 points = Annika's carrot\n"
                       "50 points = water\n"
                       "30 points = sigma\n"
                       "Run %buy <item> to purchase.")
        elif cmdname == 'buy':
            if len(cmdlist) >= 2:
                item = ' '.join(cmdlist[1:])
                prices = {"bamboo": 10, "Annika's carrot": 100, "water": 50, "sigma": 30}
                if item in prices:
                    price = prices[item]
                    if vars.bank.get(user, 0) >= price:
                        vars.bank[user] -= price
                        sendmsg = add_to_inventory(user, item)
                    else:
                        sendmsg = f"Not enough points to buy {item}. You need {price - vars.bank.get(user, 0)} more points."
                else:
                    sendmsg = "Item not found in the shop."
            else:
                sendmsg = 'Please specify an item to buy.'
        elif cmdname == 'inventory':
            user_inventory = vars.inventory.get(user, [])
            sendmsg = f"{user}'s inventory: {', '.join(user_inventory) if user_inventory else 'empty'}"
        elif cmdname == 'urbdict':
            if len(cmdlist) >= 2:
                term = ' '.join(cmdlist[1:])
                sendmsg = search_urbandict(term)
            else:
                sendmsg = 'Please provide a term to search in Urban Dictionary.'
        elif cmdname == 'ddg':
            if len(cmdlist) >= 2:
                query = ' '.join(cmdlist[1:])
                sendmsg = search_ddg(query)
            else:
                sendmsg = 'Please provide a query to search.'
        elif cmdname == 'math':
            if len(cmdlist) >= 2:
                expression = ' '.join(cmdlist[1:])
                sendmsg = solve_math(expression)
            else:
                sendmsg = 'Please provide a math expression to solve.'
        elif cmdname == 'newnym':
            sendmsg = f"@{user} SIGNALING A NEWNYM!"
        elif cmdname == 'tripmsg':
            if len(cmdlist) >= 3:
                trip = cmdlist[1]
                message = ' '.join(cmdlist[2:])
                vars.messages[trip] = message
                sendmsg = f"Message for trip {trip} set: {message}"
            else:
                sendmsg = 'Please provide a trip and a message.'
        # Handle additional commands here

        if sendmsg:
            ws.send(dumps({'cmd': 'chat', 'text': sendmsg}))

while True:
    result = loads(ws.recv())  # 3: receive data
    print(str(result))
    cmd = result['cmd']  # bro it doesnt let u run on the web for some reason

    if cmd == 'chat':  # if someone sent a message...
        if result['nick'] == nick: continue
        msg = result['text']
        if result['nick'] in vars.afk_users:
            del vars.afk_users[result['nick']]
            ws.send(dumps({'cmd': 'chat', 'text': f"{result['nick']} has returned from AFK."}))

        if vars.scramble_word and msg == vars.scramble_word:
            elapsed_time = time.time() - vars.scramble_start_time
            ws.send(dumps({'cmd': 'chat', 'text': f"Congratulations {result['nick']}! You unscrambled the word in {elapsed_time:.2f} seconds."}))
            vars.scramble_word = None
            vars.scramble_start_time = None
            vars.bank[result['nick']] = vars.bank.get(result['nick'], 0) + 10

        handle_command(result)

    elif cmd == 'onlineSet':
        vars.users = result['nicks']
        for i in result['users']:
            trip = i.get('trip', '(null)')
            vars.userinfo[i['nick']] = {'hash': i['hash'], 'trip': trip}
            if trip in vars.messages:
                ws.send(dumps({'cmd': 'whisper', 'nick': i['nick'], 'text': vars.messages[trip]}))
        print('Users online: ' + str(vars.users) + '\nPower by UwU senpai arigato!')

    elif cmd == 'onlineAdd':
        vars.users.append(result['nick'])
        trip = result.get('trip', '(null)')
        vars.userinfo[result['nick']] = {'hash': result['hash'], 'trip': trip}
        ws.send(dumps({'cmd': 'whisper', 'nick': result['nick'], 'text': 'I am the almighty being'}))
        if trip in vars.messages:
            ws.send(dumps({'cmd': 'whisper', 'nick': result['nick'], 'text': vars.messages[trip]}))

    elif cmd == 'onlineRemove':
        if result['nick'] in vars.users:
            vars.users.remove(result['nick'])
        if result['nick'] in vars.userinfo:
            del vars.userinfo[result['nick']]
