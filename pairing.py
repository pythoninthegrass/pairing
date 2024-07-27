#!/usr/bin/env python

import csv
import random
# import sqlite3
from datetime import datetime
from pathlib import Path

"""
0: Novice
1: Advanced Beginner
2: Competent
3: Proficient
4: Expert
"""

# TODO: Add a database to store the pairing history

today = datetime.now().strftime('%Y-%m-%d')

people = {}
dont_pair = []
pairings = []


def load_people():
    """
    Load people from the 'people.csv' file and populate the global 'people' dictionary.
    Only includes people with today's date.
    """
    global people
    with open(Path(__file__).parent / 'people.csv') as f:
        for line in f:
            if line.startswith('name'):
                continue
            name, level, date = line.strip().split(',')
            if date == today:
                people[name] = int(level)


def load_exclusions():
    """
    Load exclusions from the 'exclude.csv' file and populate the global 'dont_pair' list.
    Each row in the file represents a pair of people who should not be paired together.
    """
    global dont_pair
    exclusion_file = Path(__file__).parent / 'exclude.csv'
    if exclusion_file.exists():
        with open(exclusion_file, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    dont_pair.append({row[0], row[1]})


def get_dont_pair_set(name):
    """
    Get the set of people who should not be paired with the given name.

    Args:
    name (str): The name of the person to check exclusions for.

    Returns:
    set: A set of names that should not be paired with the given name,
         or None if there are no exclusions.
    """
    if not dont_pair:
        return None

    dont_pair_set = set()
    for pair in dont_pair:
        if name in pair:
            dont_pair_set.update(person for person in pair if person != name)
    return dont_pair_set


def main():
    load_people()
    load_exclusions()

    # Sort people by skill level, but introduce some randomness
    sorted_people = sorted(people.items(), key=lambda x: (x[1], random.random()))
    paired = set()

    # Handle the case of odd number of people
    if len(sorted_people) % 2 != 0:
        high_skill_group = sorted_people[-3:]  # Take the three highest skilled people
        names = sorted([person[0] for person in high_skill_group])
        pairings.append(f"{names[0]}, {names[1]}, and {names[2]}")
        paired.update(names)
        sorted_people = sorted_people[:-3]

    # Pair people based on skill level with some randomness
    while len(sorted_people) > 1:
        current_person = sorted_people.pop(0)
        dont_pair_set = get_dont_pair_set(current_person[0])

        # Create a window of potential pairs
        window_size = min(len(sorted_people), max(2, len(sorted_people) // 3))
        potential_pairs = sorted_people[:window_size]
        random.shuffle(potential_pairs)

        paired_successfully = False
        for potential_pair in potential_pairs:
            if dont_pair_set is None or potential_pair[0] not in dont_pair_set:
                pair = sorted([current_person[0], potential_pair[0]])
                pairings.append(f"{pair[0]} and {pair[1]}")
                paired.add(current_person[0])
                paired.add(potential_pair[0])
                sorted_people.remove(potential_pair)
                paired_successfully = True
                break

        # If no pair was found, add the person back to be paired later
        if not paired_successfully:
            insert_index = random.randint(0, len(sorted_people))
            sorted_people.insert(insert_index, current_person)

    # Handle any remaining unpaired person
    if sorted_people:
        pairings.append(sorted_people[0][0])

    # Sort and print all pairings
    for pairing in sorted(pairings):
        print(pairing)


if __name__ == '__main__':
    main()
