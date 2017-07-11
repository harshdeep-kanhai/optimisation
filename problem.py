import numpy as np
from matplotlib import pyplot as plt
import pulp

# setting up as a maximization problem
problem = pulp.LpProblem('Banner Chemicals', pulp.LpMaximize)

# setting up decision variables
high_grade_barrels = pulp.LpVariable('High Grade Barrels', lowBound=0, cat='Integer')
supreme_grade_barrels = pulp.LpVariable('Supreme Grade Barrels', lowBound=0, cat='Integer')

# objective function
profit = 80 * high_grade_barrels + 200 * supreme_grade_barrels

problem += profit

# constraints
additive_a = 3*high_grade_barrels + 2 * supreme_grade_barrels
additive_b = high_grade_barrels + 3 * supreme_grade_barrels
capacity = high_grade_barrels + supreme_grade_barrels

problem += (capacity <= 110)
problem += (additive_a <= 300)
problem += (additive_b <= 280)

print(problem)

# solving the LP using the default solver
optimization_result = problem.solve()

# validating for optimal solution
assert optimization_result == pulp.LpStatusOptimal

# displaying the results
for barrels in (high_grade_barrels, supreme_grade_barrels):
    print('Optimal weekly number of {} to produce: {:1.0f}'.format(barrels.name, barrels.value()))
print("profit: $",80* high_grade_barrels.value() + 200* supreme_grade_barrels.value())

print("validation")

fig, ax = plt.subplots(figsize=(10, 10))
xh = np.linspace(0, 100)

# plot the constraints again
plt.plot(xh, 110 - xh, lw=3, label='Max Plant Capacity')
plt.plot(xh, (300 - 3*xh)/2, lw=3, label='Additive A')
plt.plot(xh, (280 - xh)/3, lw=3, label='Additive B')
plt.plot(np.zeros_like(xh), xh, lw=3, label='XH non-negative')
plt.plot(xh, np.zeros_like(xh), lw=3, label='XS non-negative')

# plot the possible (xh, xs) pairs
pairs = [(xh, xs) for xh in np.arange(101)
                for xs in np.arange(101)
                if (xh + xs) <= 110
                and (3 * xh + 2* xs) <= 300
                and (xh + 3 * xs) <=280]

# split these into our variables
xh, xs = np.hsplit(np.array(pairs), 2)

# caculate the objective function at each pair
z = 80*xh + 200*xs  # the objective function

# plot the results
plt.scatter(xh, xs, c=z, cmap='jet', label='profit', zorder=3)

# labels and stuff
cb = plt.colorbar()
cb.set_label('profit', fontsize=14)
plt.xlabel('XH (no. of high grade barrel)', fontsize=16)
plt.ylabel('XS (no. of supreme grade barrel)', fontsize=16)
plt.xlim(-0.5, 100)
plt.ylim(-0.5, 100)
plt.legend(fontsize=14)
plt.show()

