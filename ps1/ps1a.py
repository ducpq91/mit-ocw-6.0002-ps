###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here

    import os
    os.chdir("C:\\Users\\Duc Pham\\temp\\MIT\\MIT OCW intro course\\6.0002\\ps1")
    content = open(filename, "r")
    cow_data = content.read()
    content.close()
    cow_dict = {}
    for cow in cow_data.split("\n"):
        name, wt = cow.split(",")
        cow_dict[name] = int(wt)
    return cow_dict

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    default_limit = limit
    trip_list = []
    cows_clone = cows.copy()
    trip = []
    while len(cows_clone) > 0:

        take = [cow for cow in cows_clone.keys() if cows_clone[cow] == max(cows_clone.values())]
        take = take[0]
        trip.append(take)
        limit -= cows_clone[take]
        cows_clone.pop(take)

        while True:
            if limit == 0:
                trip_list.append(trip)
                trip = []
                limit = default_limit
                break
            else:
                take = [cow for cow in cows_clone.keys() if cows_clone[cow] <= limit]
                if len(take) == 0:
                    trip_list.append(trip)
                    trip = []
                    limit = default_limit
                    break
                else:
                    take_val = [cows_clone.get(cow) for cow in take]
                    take.sort(key = lambda take_val: take_val, reverse = True)
                    take = take[0]
                    #print(trip)
                    trip.append(take)
                    limit -= cows_clone[take]
                    cows_clone.pop(take)
                    continue
    return trip_list

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    cow_data = cows.copy()
    current_best = None
    current_length = len(cow_data)

    for iti in get_partitions(cow_data):

        if len(iti) <= current_length:
            for trip in iti:
                trip_val = sum([cow_data.get(cow) for cow in trip])
                if trip_val <= limit:
                    if trip == iti[-1]:
                        current_length = len(iti)
                        current_best = iti
                    else:
                        continue
                else:
                    break
        else:
            continue

    return current_best

# alternate brute force (slower)
def brute_force_cow_transport_alter(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    cow_data = cows.copy()
    current_best = None
    current_length = len(cow_data)

    for iti in get_partitions(cow_data):

        for i in range(0, len(iti)):

            trip_val = [cow_data.get(cow) for cow in iti[i]]
            if sum(trip_val) <= limit:
                if i == len(iti) - 1:
                    if len(iti) < current_length:
                        current_length = len(iti)
                        current_best = iti
                    else:
                        continue
                else:
                    continue
            else:
                break

    return current_best

# Problem 4

def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    import time
    cow_dict = load_cows('ps1_cow_data.txt')

    start = time.time()
    greedy_iti = greedy_cow_transport(cow_dict)
    end = time.time()
    print("Number of trips by greedy algo is", len(greedy_iti), ". Time taken is", end - start, "seconds.")

    start = time.time()
    bf_iti = brute_force_cow_transport(cow_dict)
    end = time.time()
    print("Number of trips by brute-force algo is", len(bf_iti), ". Time taken is", end - start, "seconds.")

    start = time.time()
    bf_iti_alter = brute_force_cow_transport_alter(cow_dict)
    end = time.time()
    print("Number of trips by brute-force algo alter is", len(bf_iti_alter), ". Time taken is", end - start, "seconds.")
