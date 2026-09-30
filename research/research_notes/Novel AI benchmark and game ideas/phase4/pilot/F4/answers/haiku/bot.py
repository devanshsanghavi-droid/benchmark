"""
Brackwater bot: Safe stake maximization with tide learning and defense.
Strategy: Stake land and high fens (safe), learn tide patterns, defend when needed.
"""
from collections import defaultdict
from bot_api import Grid


class Bot:
    def __init__(self, player, game_info):
        self.g = Grid(game_info)
        self.player = player
        self.flooded_history = []
        self.flood_counts = defaultdict(int)

        # Cell values: prefer land and high fens
        self.cell_values = []
        for c in range(self.g.N):
            if self.g.terrain[c] == "#" or c == self.g.enemy_hub or c == self.g.my_hub:
                self.cell_values.append(0)
            elif self.g.elev[c] == 3:  # Land (never floods)
                self.cell_values.append(100)
            elif self.g.elev[c] == 2:  # High fen (rarely floods)
                self.cell_values.append(40)
            elif self.g.elev[c] == 1:  # Fen (sometimes floods)
                self.cell_values.append(12)
            elif self.g.elev[c] == 0:  # Low fen (often floods)
                self.cell_values.append(4)
            else:
                self.cell_values.append(0)

    def should_avoid(self, cell, turn):
        """Check if a cell is too risky to stake right now."""
        if turn > 120:
            return False  # Late game, need all resources

        # Avoid cells that flood frequently
        if self.flood_counts[cell] >= 3:
            return self.g.elev[cell] < 2  # Only avoid non-safe cells

        return False

    def get_stake_targets(self, obs, turn):
        """Find best cells to stake."""
        my_stakes = set(obs["stakes"])
        targets = []

        for c in range(self.g.N):
            if c in my_stakes or self.g.terrain[c] == "#":
                continue
            if c == self.g.enemy_hub or c == self.g.my_hub:
                continue

            value = self.cell_values[c]
            if value == 0:
                continue

            if self.should_avoid(c, turn):
                value *= 0.3

            targets.append((value, c))

        targets.sort(reverse=True)
        return [c for _, c in targets[:20]]

    def act(self, obs):
        turn = obs["turn"]

        # Track flooding
        flooded_set = set(obs["flooded"])
        self.flooded_history.append(flooded_set)
        for c in flooded_set:
            self.flood_counts[c] += 1

        # Get stake targets
        targets = self.get_stake_targets(obs, turn)

        # Compute defense needs
        my_stakes = set(obs["stakes"])
        defense_needs = {}
        for stake_cell in my_stakes:
            enemy_nearby = sum(obs["enemy_crews"].get(nc, 0)
                              for nc in self.g.neighbors(stake_cell) + [stake_cell])
            if enemy_nearby > 0:
                defense_needs[stake_cell] = enemy_nearby

        # Assign orders
        orders = {}

        if targets:
            dist_to_target = self.g.bfs(targets)
        else:
            dist_to_target = None

        for crew_id, crew_cell in obs["crews"].items():
            # Priority: Defend threatened stakes
            if crew_cell in defense_needs:
                orders[crew_id] = "H"
                continue

            # Secondary: Move to stake targets
            if dist_to_target is not None:
                d = dist_to_target[crew_cell]
                if d < 0:
                    orders[crew_id] = "H"
                elif d == 0:
                    orders[crew_id] = "K"
                else:
                    orders[crew_id] = self.g.step_toward(crew_cell, dist_to_target)
            else:
                orders[crew_id] = "H"

        # Recruitment
        recruit = False
        if obs["recruit_cost"] <= obs["grain"]:
            n_crews = len(obs["crews"])
            grain = obs["grain"]
            cost = obs["recruit_cost"]

            # Simple recruitment strategy: recruit when we can afford it and need crew
            if turn < 30 and n_crews < 12:
                recruit = True
            elif turn < 80 and n_crews < 15 and grain > cost * 3:
                recruit = True
            elif turn < 120 and n_crews < 17 and grain > cost * 5:
                recruit = True

        return {
            "orders": orders,
            "recruit": recruit
        }
