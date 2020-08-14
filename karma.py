class Karma:
    def __init__(self, db):
        self.db = db

    def set_karma(self, user, value):
        if self.db.exists(f"user:{user}") == 0:
            self.db.hset(f"user:{user}", "karma", value)
        else:
            karma = int(self.db.hget(f"user:{user}", "karma"))
            karma = int(karma) + value
            self.db.hset(f"user:{user}", "karma", str(karma))


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
        karma = self.db.hget(f"user:{user}", "karma")
        bot.send_message(chat_id=chat.id, text=user+" has "+karma+" karma")