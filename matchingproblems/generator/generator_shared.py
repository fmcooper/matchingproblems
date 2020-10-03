import numpy as np
import random

"""Functions shared between the generators."""

def create_ties_indicators(pref_lists, ties_prob):
    """Creates ties indicators.

    Creates a tag for each preference list element indicating whether
    a preference list element is tied with the next.

    Args:
        pref_lists: The preference lists to copy the shape of.
        ties_prob: The probability one element on a preference list is tied
          with the next.

    Returns:
        ties_indicators for the given preference lists
    """
    ties_choices = np.array([0, 1])
    p=[1 - ties_prob, ties_prob]
    
    ties_indicators = []
    for pref_list in pref_lists:
        ties_indicators.append(
            np.random.choice(ties_choices, len(pref_list), p=p))

    return ties_indicators


def create_linear_distribution(number_agents, skew):
    """Creates a linear distribution.

    Creates a distribution of length number_agents, which represents the 
    popularity of the different men or women. 

    Args:
        number_agents: The number of agents in the instance.
        skew: A skew of x indicates that the most popular person is x times more
        popular than the least popular person.

    Returns:
        The distribution of people's popularity as a list. E.g. with 
        number_agents = 4 and skew = 10, we obtain the following distribution:

        [0.04545455 0.18181818 0.31818182 0.45454545]
    """

    # First a list is created with the first element equalling 1, the final 
    # element equalling 1.0 * skew and all other elements linearly distributed
    # between the two. 
    # E.g. for a skew of 10 and 4 residents we create the list: 
    # [1.0, 4.0, 7.0, 10.0]
    distribution = [0.0] * number_agents
    distribution[0] = 1.0
    for x in range(1, number_agents):
        distribution[x] = 1.0 + float(x * (skew - 1)/(number_agents - 1))

    # Return the distribution with sum of elements equalling 1
    return distribution / np.sum(distribution)


def create_string_pref(pref_list, ties_indicators):
    """Creates preference list string for output.

    Args:
        pref_list: The preference list of an agent.
        ties_indicators: Whether elements of this preference list are tied.

    Returns:
        A preference list string for output.
    """
    string_pref = []
    in_tie = False
    for i in range(len(pref_list)):
        if not in_tie and ties_indicators[i] and i < len(pref_list) - 1:
            string_pref.append('(' + str(pref_list[i]))
            in_tie = True
        elif in_tie and not ties_indicators[i]:
            string_pref.append(str(pref_list[i]) + ')')
            in_tie = False
        elif i == len(pref_list) - 1 and in_tie:
            string_pref.append(str(pref_list[i]) + ')')
        else:
            string_pref.append(str(pref_list[i]))
    return string_pref
       

def create_pref_lists_original(
    n1, n2, minpreflistlength, maxpreflistlength, ties1, skew):
    """Creates preference lists not dependent on other preference lists.

    Creates 2D lists of agent preference lists, according to a linear 
    distribution determined by the skew. 

    Args:
        n1: The number of agents to generate preference lists for.
        n2: The number of agents which may be ranked.
        minpreflistlength: The minimum length of preference lists.
        maxpreflistlength: The maximum length of preference lists.
        ties1: The probability a preference list element is tied with another.
        skew: A skew of x indicates that the most popular person is x times more
        popular than the least popular person.

    Returns:
        A 2D preference list.
        A 2D ties indicator list.
    """
    random_complete_prefs_agent1 = np.arange(1, n2 + 1)
    random.shuffle(random_complete_prefs_agent1)
    distribution = create_linear_distribution(n2, skew)

    pref_lists_agent1 = [[] for i in range(n1)]
    for x in range(n1):
        length_plist = np.random.randint(
            minpreflistlength, maxpreflistlength + 1)
        pref_list_agent1 = np.random.choice(
            random_complete_prefs_agent1, 
            length_plist, 
            replace=False, 
            p=distribution)
        pref_lists_agent1[x] = pref_list_agent1

    ties_indicator_agent1 = create_ties_indicators(pref_lists_agent1, ties1)
    return pref_lists_agent1, ties_indicator_agent1


def create_pref_lists_from_other_lists(pref_lists_agent1, n2, ties2):
    """Creates preference lists dependent on other preference lists.

    Creates random preference lists, according to the given preference lists 
    (an agent of type 2 may only rank an agent of type 1 that ranks them). 

    Args:
        pref_lists_agent1: The existing preference lists.
        args: User chosen instance parameter information.

    Returns:
        A 2D list of hospitals preference lists over residents.
    """
    prefs_lists_agent2 = [[] for i in range(n2)]
    for i, pref_list_agent1 in enumerate(pref_lists_agent1):
        for agent1_num in pref_list_agent1:
            prefs_lists_agent2[agent1_num - 1].append(i + 1)
    
    for prefs_list_agent2 in prefs_lists_agent2:
        random.shuffle(prefs_list_agent2)

    ties_indicator_agent2 = create_ties_indicators(prefs_lists_agent2, ties2)
    return prefs_lists_agent2, ties_indicator_agent2


def create_quotas(n, sum_q):
    """Returns evenly distributed quotas. 

    Args:
        n: The number of agents.
        sum_q: The sum of quotas to distribute.

    Returns:
        Evenly distributed upper and lower quotas.
    """
    quotas = []

    quotient = int(sum_q / n)
    remainder = int(sum_q % n)
    for i in range(n):
        quotas.append(quotient)
        if i < remainder:
            quotas[i] += 1

    return quotas
