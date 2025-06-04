import random
import math

# All possible box values
all_box_values = [
    1, 10, 50, 100, 250, 500, 750, 1000,
    2500, 5000, 7500, 10000, 15000, 20000, 25000,
    50000, 75000, 100000, 150000, 200000,
    250000, 300000, 400000, 500000, 750000, 1000000
]

def assign_beta(alpha):
    if alpha < 0.3:
        return 0.50
    elif alpha < 0.5:
        return 0.40
    elif alpha < 0.7:
        return 0.30
    else:
        return 0.20

def acceptance_probability(B, E, alpha, k=5):
    exponent = -k * (B - alpha * E)
    if exponent > 700:
        return 0.0
    elif exponent < -700:
        return 1.0
    return 1 / (1 + math.exp(exponent))

# Strategy functions
def simple_strategy(remaining):
    return (max(remaining) + min(remaining)) / 2

def expected_value_strategy(remaining):
    return sum(remaining) / len(remaining)

def dynamic_strategy(remaining, alpha):
    E = sum(remaining) / len(remaining)
    return alpha * E

def aggressive_strategy(remaining, beta=0.3):
    return min(remaining) + beta * (max(remaining) - min(remaining))

def smart_hybrid_strategy(remaining, alpha):
    E = sum(remaining) / len(remaining)
    simple = (max(remaining) + min(remaining)) / 2
    return alpha * E + (1 - alpha) * simple

# ✅  simulate_game Function
def simulate_game(strategy_func, prize_values, alpha=0.7, beta=0.3, verbose=False, sim_num=1, strategy_name=""):
    remaining_values = prize_values.copy()
    opened = random.sample(remaining_values, 21)
    for val in opened:
        remaining_values.remove(val)

    bank_payment = 0
    offer_rounds = [5, 2]  # Offers are made when 5 and 2 boxes remain

    if verbose:
        print(f"\n=== Simulation {sim_num}, Strategy: {strategy_name} ===")

    for boxes_left in range(5, 0, -1):
        if boxes_left < 5:
            opened_box = random.choice(remaining_values)
            remaining_values.remove(opened_box)

        if boxes_left in offer_rounds:
            E = sum(remaining_values) / len(remaining_values)

            if strategy_func.__name__ in ['dynamic_strategy', 'smart_hybrid_strategy']:
                B = strategy_func(remaining_values, alpha)
            elif strategy_func.__name__ == 'aggressive_strategy':
                B = strategy_func(remaining_values, beta)
            else:
                B = strategy_func(remaining_values)

            B = math.ceil(B)
            p_accept = acceptance_probability(B, E, alpha)
            rand_val = random.random()
            offer_accepted = rand_val < p_accept

            if verbose:
                print(f"Boxes remaining: {boxes_left}")
                print(f"Remaining values: {[str(v) + ' TL' for v in sorted(remaining_values)]}")
                print(f"Alpha (risk factor): {alpha:.3f}")
                if strategy_func.__name__ == 'aggressive_strategy':
                    print(f"Beta (aggressiveness): {beta:.3f}")
                print(f"Expected Value (E): {E:,.2f} TL")
                print(f"Bank's Offer (B): {B:,} TL")
                print(f"Acceptance Probability: {p_accept:.2%}")
                print(f"Was the offer accepted? {'Yes' if offer_accepted else 'No'}")
                print("-" * 40)

            if offer_accepted:
                bank_payment = B
                break  # Sadece kabul edilirse oyun sona ersin

    if bank_payment == 0:
        bank_payment = random.choice(remaining_values)
        if verbose:
            print(f"At the end of the game, one of the remaining boxes was chosen: {bank_payment:,.2f} TL")

    return bank_payment

# Run and compare all strategies
def run_all_strategies(num_sim=100, verbose=False):
    strategies = {
        "Simple": simple_strategy,
        "Expected Value": expected_value_strategy,
        "Dynamic": dynamic_strategy,
        "Aggressive": aggressive_strategy,
        "Smart Hybrid": smart_hybrid_strategy
    }

    alphas = [
        0.74, 0.28, 0.66, 0.41, 0.91, 0.57, 0.37, 0.79, 0.48, 0.25,
        0.85, 0.72, 0.52, 0.46, 0.29, 0.58, 0.43, 0.93, 0.64, 0.27,
        0.87, 0.32, 0.76, 0.68, 0.49, 0.35, 0.59, 0.82, 0.24, 0.65,
        0.31, 0.44, 0.92, 0.39, 0.84, 0.23, 0.73, 0.34, 0.62, 0.77,
        0.71, 0.38, 0.63, 0.45, 0.33, 0.81, 0.53, 0.36, 0.30, 0.26,
        0.47, 0.86, 0.22, 0.61, 0.42, 0.55, 0.78, 0.40, 0.54, 0.50,
        0.83, 0.67, 0.60, 0.20, 0.69, 0.51, 0.80, 0.75, 0.90, 0.21,
        0.70, 0.56, 0.95, 0.88, 0.66, 0.59, 0.46, 0.35, 0.53, 0.74,
        0.29, 0.68, 0.43, 0.32, 0.26, 0.91, 0.34, 0.60, 0.22, 0.44,
        0.40, 0.36, 0.82, 0.48, 0.30, 0.28, 0.63, 0.23, 0.25, 0.38
    ]

    results = {name: 0 for name in strategies.keys()}

    for i in range(num_sim):
        alpha = alphas[i % len(alphas)]
        beta = assign_beta(alpha)

        for name, func in strategies.items():
            if name in ["Dynamic", "Smart Hybrid"]:
                pay = simulate_game(func, all_box_values, alpha=alpha, verbose=verbose, sim_num=i + 1, strategy_name=name)
            elif name == "Aggressive":
                pay = simulate_game(func, all_box_values, alpha=alpha, beta=beta, verbose=verbose, sim_num=i + 1, strategy_name=name)
            else:
                pay = simulate_game(func, all_box_values, alpha=alpha, verbose=verbose, sim_num=i + 1, strategy_name=name)

            results[name] += pay

    print(f"\n{'Strategy':<15} | {'Average Payment':>20}")
    print("-" * 40)
    for name in strategies.keys():
        avg = results[name] / num_sim
        print(f"{name:<15} | {math.ceil(avg):>20,} TL")

    best_strategy = min(results, key=results.get)
    print(f"\nThe strategy that minimizes the bank's payment: {best_strategy}")

# Entry point
if __name__ == "__main__":
    run_all_strategies(num_sim=100, verbose=True)
