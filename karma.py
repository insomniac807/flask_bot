class Karma:
    def __init__(self, db):
        self.db = db

    def set_karma(self, user, value):
        if self.db.exists(user) == 0:
            self.db.set(user, value)
        else:
            karma = int(self.db.get(user))
            karma = karma + value
            self.db.set(user, karma)


    def handle_karma(self, string, chat, bot):
        if "++" in string:
            user = string.split("++")[0]
            self.set_karma(user, 1)
        elif "—" in string:
            user = string.split("—")[0]
            self.set_karma(user, -1)
        else:
            user = string.split(" ")[1]
            self.set_karma(user, 0)
        karma = self.db.get(user) 
        bot.send_message(chat_id=chat.id, text=user+" has "+karma+" karma")