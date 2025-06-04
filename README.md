# MONTE-CARLO-DEAL-OR-NO-DEAL-SIMULATION
MONTE CARLO SIMULATION DEAL OR NO DEAL 
 1 Project 1: Optimal Bank Offer Strategy in Deal or
 No Deal

 1.1 Project Overview
 In this project, students will take on the role of the bank in the game ”Deal or No
 Deal.” The goal is to determine the best strategy for making offers to players in order to
 minimize the bank’s expected payout. The key challenge is to develop a **Monte Carlo
 simulation** that models different offer strategies and determines the most cost-effective
 one.

 1.2 Simulation Setup- The game is considered in the final five-box stage.- The remaining five boxes contain
 random monetary values.- The bank must decide on an offer based on the remaining
 values.- The player has a probabilistic decision function to accept or reject the offer.

 1.3 Bank Offer Strategy
 A simple baseline strategy is proposed:
 B = max(V)+min(V)
 where:
 • B =Bank’s offer.
 • V =Set of remaining box values.
 • max(V) = Highest remaining prize.
 • min(V) = Lowest remaining prize.

 2
 Students must analyze whether this is the best strategy or find an improved method
 that minimizes the bank’s expected payout.

 1.4 Acceptance Probability Function
 A sigmoid-based function will be used to model the player’s decision-making process:
 Paccept =
 where:
 • B =Bank’s offer.
 1
 1 +e−k·(B−α·E)
 • E =Expected value of the remaining boxes.
 • α =Risk factor of the player (e.g., 0.8).
 1
• k =Sensitivity of the player’s decision-making, suggested value: **5**.
 Students can implement this function in Python or VBA and test different offer strate
gies to determine which results in the lowest average payout for the bank.
