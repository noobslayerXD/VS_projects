import SMPFuncs as SMP

# Example usage of the SMPFuncs module to calculate the union of independent events
probabilities = [0.01, 0.02]
result = SMP.union_of_independent_events(probabilities)
print(f"The probability of the union of independent events is: {result:.4f}")

# Example usage of the SMPFuncs module to apply Bayes' theorem
prior = 0.5
likelihood = 0.01
evidence = 0.00001
posterior = SMP.bayes_rule(prior, likelihood, evidence)
print(f"The posterior probability is: {posterior:.4f}")



