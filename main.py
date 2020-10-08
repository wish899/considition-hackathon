import api
from game_layer import GameLayer

api_key = "e506eaf0-ccdd-42a1-998d-7445c6cdced2"   # TODO: Your api key here
# The different map names can be found on considition.com/rules
map_name = "training1"  # TODO: You map choice here. If left empty, the map "training1" will be selected.

game_layer = GameLayer(api_key)


def main():
    game_layer.new_game(map_name)
    print("Starting game: " + game_layer.game_state.game_id)
    game_layer.start_game()
    while game_layer.game_state.turn < game_layer.game_state.max_turns:
        take_turn()
    print("Done with game: " + game_layer.game_state.game_id)
    print("Final score was: " + str(game_layer.get_score()["finalScore"]))


def take_turn():
    state = game_layer.game_state
    count = len(game_layer.game_state.available_residence_buildings) - 1
    if len(state.residences) < 1:
        for i in range(len(state.map)):
            for j in range(len(state.map)):
                if state.map[i][j] == 0:
                    if i == j:
                        game_layer.place_foundation((i, j), game_layer.game_state.available_residence_buildings[count].building_name)
                        count -= 1
                        if count <= 0: break
    else:
        for residence in state.residences:
            if residence.build_progress < 100:
                game_layer.build((residence.X, residence.Y))
            elif residence.health < 50:
                game_layer.maintenance((residence.X, residence.Y))
            elif residence.temperature < 18:
                blueprint = game_layer.get_residence_blueprint(residence.building_name)
                energy = blueprint.base_energy_need + 0.5 \
                            + (residence.temperature - state.current_temp) * blueprint.emissivity / 1 \
                            - residence.current_pop * 0.04
                game_layer.adjust_energy_level((residence.X, residence.Y), energy)
            elif residence.temperature > 24:
                blueprint = game_layer.get_residence_blueprint(residence.building_name)
                energy = blueprint.base_energy_need - 0.5 \
                            + (residence.temperature - state.current_temp) * blueprint.emissivity / 1 \
                            - residence.current_pop * 0.02
                game_layer.adjust_energy_level((residence.X, residence.Y), energy)
            else:
                break
        game_layer.wait()

    for message in game_layer.game_state.messages:
        print(message)
    for error in game_layer.game_state.errors:
        print("Error: " + error)


if __name__ == "__main__":
    main()
