import json

emoji = {
    "0": "\N{Large Red Circle}",
    "1": "\N{Large Green Circle}",
    "2": "\N{Large Orange Circle}",
    "3": "\N{Large Blue Circle}",
    "4": "\N{Large Brown Circle}",
    "5": "\N{Large Purple Circle}",
    "6": "\N{Large Red Square}",
    "7": "\N{Large Green Square}",
    "8": "\N{Large Orange Square}",
    "9": "\N{Large Blue Square}",
    "10": "\N{Large Brown Square}",
    "11": "\N{Large Purple Square}",
    "12": "\N{Large Orange Diamond}",
    "13": "\N{Large Blue Diamond}",
    "14": "\N{Heavy Black Heart}",
    "15": "\N{Green Heart}",
    "16": "\N{Orange Heart}",
    "17": "\N{Blue Heart}",
    "18": "\N{Brown Heart}",
    "19": "\N{Purple Heart}",
}

json.dump(emoji, open("./poll_emoji.json", "a"))
