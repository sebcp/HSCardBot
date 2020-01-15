from telegram.ext import Updater, CommandHandler
import json,urllib
import requests
import os


def gettoken():
    clientid = '1f01b88fc4824d2281fc3575882a2b12'
    secret = 'ZZmc5mkvKhydoNZ5VOhT1GWqxs7sGVI3'

    os.system('curl -u ' + clientid +':'+secret+' -d grant_type=client_credentials https://us.battle.net/oauth/token > out.txt')
    with open("out.txt","r") as f:
        txt = f.readline()
        token = ""
        state = False
        for x in txt:
            if x==":":
                state = True
            elif state == True and x!='"':
                token += x
            elif x == '"' and len(token)>1:
                break
    return token


def start(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id,
                     "I'm a bot made for displaying Hearthstone cards. Type /card Card Name to see the "
                     "card you're looking for. (The /card command is case insensitive)")


def fetchid(args):
    with open("cards.collectible.json", "r") as f:
        cards_dict = json.load(f)
    for card in cards_dict:
        if str(card["name"]).lower()==" ".join(args).lower():
            return str(card["dbfId"])


def get_url(token, id):
    url_json = 'https://us.api.blizzard.com/hearthstone/cards/'+id+'?locale=en_US&access_token='+token
    with urllib.request.urlopen(url_json) as url:
        data = json.loads(url.read().decode())
    return str(data["image"])
   

def card(bot, update, args):
    token = gettoken()
    chat_id = update.message.chat_id
    id = fetchid(args)
    url = get_url(token,id)
    bot.send_photo(chat_id, photo=url)



def main():
    updater = Updater("969964976:AAFV-HvFbtlw-NJLJObaUyVyG_Dk6Q8O4ME")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("card", card, pass_args=True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
