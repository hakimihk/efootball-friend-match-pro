import random

def generate_fixtures(player_list):
    """Generates Random Matchups"""
    random.shuffle(player_list)
    fixtures = []
    for i in range(0, len(player_list), 2):
        fixtures.append((player_list[i], player_list[i+1]))
    return fixtures

# Example Output for 8 players:
# [(@user1 vs @user4), (@user2 vs @user8)...]
