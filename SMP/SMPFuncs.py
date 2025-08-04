#Union of independent events
def union_of_independent_events(probabilities):
    """
    Calculate the probability of the union of independent events.

    :param probabilities: A list of probabilities of independent events.
    :return: The probability of the union of the events.
    """
    if not probabilities:
        return 0.0

    # Calculate the probability of the intersection of the complements
    prob_intersection_complement = 1.0
    for p in probabilities:
        prob_intersection_complement *= (1 - p)

    # The probability of the union is 1 minus the probability of the intersection of complements
    return 1 - prob_intersection_complement

# bayes rule
def bayes_rule(prior, likelihood, evidence):
    """
    Apply Bayes' theorem to calculate the posterior probability.

    :param prior: The prior probability of the hypothesis.
    :param likelihood: The likelihood of the evidence given the hypothesis.
    :param evidence: The total probability of the evidence.
    :return: The posterior probability of the hypothesis given the evidence.
    """
    if evidence == 0:
        return 0.0
    return (prior * likelihood) / evidence

# Law of total probability
def law_of_total_probability(evidence, *hypotheses):
    """
    Apply the law of total probability to calculate the total probability of the evidence.

    :param evidence: The evidence for which to calculate the total probability.
    :param hypotheses: A list of tuples containing (prior, likelihood) for each hypothesis.
    :return: The total probability of the evidence.
    """
    total_prob = 0.0
    for prior, likelihood in hypotheses:
        total_prob += SMP.bayes_rule(prior, likelihood, evidence)
    return total_prob
