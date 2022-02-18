#!/usr/bin/env python3
"""
appspot: Receives a numeric value from the user and executes the function
find_players_pairs if the parameter is correct
"""
import sys
import requests


def find_players_pairs(data, inches, pairs_list=[]):
    """
    Prints a list of all pairs of players whose height in inches adds up to
    the integer input as parameter 'inches'.
    """
    # Base case when all players have been processed
    if len(data) <= 1:
        return pairs_list
    # Take first and last players of the list
    player_1 = data[0]
    player_2 = data[-1]
    result = int(player_1['h_in']) + int(player_2['h_in'])
    # Evaluate if the result match with inches parameter
    if result > inches:
        find_players_pairs(data[:-1], inches, pairs_list)
    elif result < inches:
        find_players_pairs(data[1:], inches, pairs_list)
    else:
        pairs_list.append((player_1, player_2))
        checker = -2
        index_0 = len(data) * -1
        while checker != index_0:
            if player_2['h_in'] != data[checker]['h_in']:
                break
            player_2 = data[checker]
            pairs_list.append((player_1, player_2))
            checker -= 1
        find_players_pairs(data[1:], inches, pairs_list)
    return pairs_list


def print_players_list(pairs_list):
    """
    Prints the names of tuple players in a list
    """
    for player_1, player_2 in pairs_list:
        print_player_names(player_1, player_2)


def print_player_names(player_1, player_2):
    """
    Prints the name and last name of two players
    """
    print("- {} {} \t {} {}".format(player_1['first_name'],
                                    player_1['last_name'],
                                    player_2['first_name'],
                                    player_2['last_name']))


def main():
    """

    """
    try:
        num_input = sys.argv[1]
        if not num_input.isdigit():
            raise TypeError

        r = requests.get('https://mach-eight.uc.r.appspot.com/')
        if r.status_code >= 300:
            raise

        data = r.json()
        sort_data = sorted(data['values'], key=lambda p: p['h_in'])
        pairs_list = find_players_pairs(sort_data, int(num_input))
        if not len(pairs_list):
            print("No matches found")
        print_players_list(pairs_list)

    except TypeError:
        print("Error, argument must be Integer value only")
    except IndexError:
        print("Error, no argument passed")
    except:
        print("The API does not respond")


if __name__ == "__main__":
    main()
