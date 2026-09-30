"""Random-legal reference bot (public).  Picks a uniformly random legal order for every crew
and recruits with probability 0.25 whenever recruiting is legal."""
import random
import zlib

from bot_api import Grid


class Bot:
    def __init__(self, player, game_info):
        self.g = Grid(game_info)
        self.rng = random.Random(zlib.crc32(game_info["terrain"].encode()) * 2 + player)

    def act(self, obs):
        orders = {}
        for cid, c in obs["crews"].items():
            orders[cid] = self.rng.choice(self.g.legal_orders(c))
        can = obs["grain"] >= obs["recruit_cost"] and len(obs["crews"]) < self.g.crew_cap
        return {"orders": orders, "recruit": bool(can and self.rng.random() < 0.25)}
