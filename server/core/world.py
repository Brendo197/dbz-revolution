# server/core/world.py

class World:
    def __init__(self):
        self.players = []

    def add_player(self, client):
        if client not in self.players:
            self.players.append(client)

    def remove_player(self, client):
        if client in self.players:
            self.players.remove(client)

    def update(self):
        # loop do mundo (tick)
        # futuramente: NPC, mapa, combate
        pass
