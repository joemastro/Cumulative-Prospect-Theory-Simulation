import matplotlib.pyplot as plt

class cpt:
    def __init__(self, alpha, gamma, sigma, lam):
        self.alpha = alpha
        self.gamma = gamma
        self.sigma = sigma
        self.lam = lam

        # Parameter restrictions
        if self.lam <= 1:
            raise ValueError("Lambda value must be greater than 1")
        if (self.alpha >= 1 or self.alpha <= 0) or \
           (self.gamma >= 1 or self.gamma <= 0) or \
           (self.sigma >= 1 or self.sigma <= 0):
            raise ValueError("alpha, gamma, and sigma values must be strictly between 0 and 1")

    def value_function(self, x):
        # Is the outcome a gain?
        if x >= 0:
            return x ** self.alpha
        # Is the outcome a loss?
        else:
            return -self.lam * (-x) ** self.alpha

    def prob_weight_plus(self, p):
        if p == 1: return 1
        elif p == 0: return 0
        else: return (p ** self.gamma) / ((p ** self.gamma + (1 - p ** self.gamma)) ** (1 / self.gamma))

    def prob_weight_minus(self, p):
        if p == 1: return 1
        elif p == 0: return 0
        else: return (p ** self.sigma) / ((p ** self.sigma + (1 - p ** self.sigma)) ** (1 / self.sigma))

    def expected_value(self, lottery):
        total = 0
        for i, (xi, pi) in enumerate(lottery):
            if xi >= 0:
                # Defines the aggregate sum from the ith probability to the nth probability
                w_plus_i = self.prob_weight_plus(sum([p for _, p in lottery[i:]]))
                # Check if we are at the end of the lottery
                if i < len(lottery) - 1:
                    # Defines the aggregate sum from the ith+1 probability to the nth probability
                    w_plus_i_next = self.prob_weight_plus(sum([p for _, p in lottery[i+1:]]))
                    total += self.value_function(xi) * (w_plus_i - w_plus_i_next)
                else:
                    total += self.value_function(xi) * w_plus_i
            else:
                # Defines the aggregate sum from the -mth probability to the ith+1 probability
                w_minus_i = self.prob_weight_minus(sum([p for _, p in lottery[:i+1]]))
                # Check if we are at the end of the lottery
                if i > 0:
                    # Defines the aggregate sum from the -mth probability to the ith probability
                    w_minus_i_prev = self.prob_weight_minus(sum([p for _, p in lottery[:i]]))
                    total += self.value_function(xi) * (w_minus_i - w_minus_i_prev)
                else:
                    total += self.value_function(xi) * w_minus_i
        return total

alpha = 0.88
gamma = 0.61
sigma = 0.69
lam = 2.25
agent = cpt(alpha, gamma, sigma, lam)

# A demonstration of loss aversion
print("\nThe following is a demonstration of loss aversion.\nThat is, the irrational behavior that outweighs losses over gains")

print("The value assigned to a gain of 5 is ", agent.value_function(5))
print("The value assigned to a loss of 5 is ", agent.value_function(-5))

print("Loss aversion holds here, as v(5) > v(-5)\n----------------------")

# Showing the overweighting of tails
print("To show people overweight tail end probabilities,\nwe compare extreme examlpes of lotteries to certain outcomes:")

lotteryA = [(-50, 0.001), (0, 0.999)]  # Example lottery [(xi, pi), ...]
lotteryB = [(-5, 1)]
Ev_A = agent.expected_value(lotteryA)
Ev_B = agent.expected_value(lotteryB)

print("Expected value of lottery A:", Ev_A)
print("Expected value of lottery B:", Ev_B)
if (Ev_A > Ev_B): print("Lottery A is preferred over Lottery B")
elif (Ev_A < Ev_B): print("Lottery B is preferred over Lottery A")
else: print("Lottery A and B are interchangable")

lotteryC = [(50, 0.001), (0, 0.999)]
lotteryD = [(5, 1)]
Ev_C = agent.expected_value(lotteryC)
Ev_D = agent.expected_value(lotteryD)

print("Expected value of lottery C:", Ev_C)
print("Expected value of lottery D:", Ev_D)
if (Ev_C > Ev_D): print("Lottery C is preferred over Lottery D")
elif (Ev_C < Ev_D): print("Lottery D is preferred over Lottery C")
else: print("Lottery C and D are interchangable")

# Plotting the value function on the x-value axis
x_values = list(range(-50, 51))
y_values = []
for x in x_values:
    y_values.append(agent.value_function(x))


plt.plot(x_values, y_values)
plt.title("Value Function")
plt.xlabel("x")
plt.ylabel("Value")
plt.grid(True)
plt.show()
