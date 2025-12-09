import math
import os
import re
import sys
from functools import lru_cache
from textwrap import dedent


def parse(data: str):
    blueprints = []
    pattern = re.compile(
        r"Blueprint (\d+): Each ore robot costs (\d+) ore. "
        r"Each clay robot costs (\d+) ore. "
        r"Each obsidian robot costs (\d+) ore and (\d+) clay. "
        r"Each geode robot costs (\d+) ore and (\d+) obsidian."
    )
    for line in data.strip().splitlines():
        match = pattern.match(line)
        if not match:
            continue
        idx, ore_cost, clay_cost, obs_ore, obs_clay, geo_ore, geo_obs = map(
            int, match.groups()
        )
        blueprints.append(
            (
                idx,
                (
                    (ore_cost, 0, 0),  # ore robot
                    (clay_cost, 0, 0),  # clay robot
                    (obs_ore, obs_clay, 0),  # obsidian robot
                    (geo_ore, 0, geo_obs),  # geode robot
                ),
            )
        )
    return blueprints


def max_geodes(costs, time_limit):
    max_ore_cost = max(cost[0] for cost in costs)
    max_clay_cost = costs[2][1]
    max_obs_cost = costs[3][2]

    @lru_cache(maxsize=None)
    def dfs(
        time_left,
        ore,
        clay,
        obsidian,
        ore_bots,
        clay_bots,
        obs_bots,
        geo_bots,
    ):
        if time_left == 0:
            return 0

        # Clamp resources to avoid excess state growth
        ore = min(ore, max_ore_cost * time_left - ore_bots * (time_left - 1))
        clay = min(clay, max_clay_cost * time_left - clay_bots * (time_left - 1))
        obsidian = min(
            obsidian, max_obs_cost * time_left - obs_bots * (time_left - 1)
        )

        state = (
            time_left,
            ore,
            clay,
            obsidian,
            ore_bots,
            clay_bots,
            obs_bots,
            geo_bots,
        )

        best = 0

        for robot_type, (cost_ore, cost_clay, cost_obs) in enumerate(costs):
            if robot_type == 0 and ore_bots >= max_ore_cost:
                continue
            if robot_type == 1 and clay_bots >= max_clay_cost:
                continue
            if robot_type == 2 and (obs_bots >= max_obs_cost or max_obs_cost == 0):
                continue

            wait = 0
            reqs = [
                (cost_ore, ore, ore_bots),
                (cost_clay, clay, clay_bots),
                (cost_obs, obsidian, obs_bots),
            ]

            possible = True
            for cost, have, robots in reqs:
                if cost == 0:
                    continue
                if robots == 0:
                    possible = False
                    break
                need = cost - have
                if need > 0:
                    wait = max(wait, (need + robots - 1) // robots)
            if not possible:
                continue

            total_wait = wait + 1
            if time_left - total_wait <= 0:
                continue

            new_ore = ore + ore_bots * total_wait - cost_ore
            new_clay = clay + clay_bots * total_wait - cost_clay
            new_obs = obsidian + obs_bots * total_wait - cost_obs

            new_ore_bots = ore_bots + (1 if robot_type == 0 else 0)
            new_clay_bots = clay_bots + (1 if robot_type == 1 else 0)
            new_obs_bots = obs_bots + (1 if robot_type == 2 else 0)
            new_geo_bots = geo_bots + (1 if robot_type == 3 else 0)

            best = max(
                best,
                (geo_bots * total_wait)
                + dfs(
                    time_left - total_wait,
                    new_ore,
                    new_clay,
                    new_obs,
                    new_ore_bots,
                    new_clay_bots,
                    new_obs_bots,
                    new_geo_bots,
                ),
            )

        # Option to do nothing more
        best = max(best, geo_bots * time_left)

        return best

    return dfs(time_limit, 0, 0, 0, 1, 0, 0, 0)


def part1(data: str) -> int:
    blueprints = parse(data)
    total = 0
    for idx, costs in blueprints:
        total += idx * max_geodes(costs, 24)
    return total


def part2(data: str) -> int:
    blueprints = parse(data)[:3]
    product = 1
    for _, costs in blueprints:
        product *= max_geodes(costs, 32)
    return product


def run_example() -> None:
    example = dedent(
        """\
        Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
        Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
        """
    )
    assert part1(example) == 33
    assert part2(example) == 3472
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))
