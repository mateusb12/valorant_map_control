import pygame

from agent_behavior.agent_object import Agent


def plot_teams(input_screen: pygame.Surface) -> list[Agent]:
    input_dict = {"Less": {"agent": "Chamber", "side": "attack", "x": 887, "y": 577},
                  "Aspas": {"agent": "Raze", "side": "attack", "x": 794, "y": 585},
                  "pancada": {"agent": "Omen", "side": "attack", "x": 639, "y": 602},
                  "Sacy": {"agent": "Fade", "side": "attack", "x": 475, "y": 608},
                  "saadhak": {"agent": "Breach", "side": "attack", "x": 360, "y": 613}}

    agent_pot = []

    for key, value in input_dict.items():
        new_agent = Agent(x=value["x"], y=value["y"], input_image=f"{value['agent'].lower()}.png", initial_side=value["side"],
                          input_screen=input_screen)
        new_agent.player_name = key
        new_agent.controllable = False
        agent_pot.append(new_agent)
    return agent_pot
