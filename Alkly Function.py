# --- IMPORT DEPENDENCIES ------------------------------------------------------+

from __future__ import division
import random
import math


# --- COST FUNCTION ------------------------------------------------------------+

#------The Ackley function is widely used for testing optimization algorithms. In its two-dimensional
#------form, as shown in the plot above, it is characterized by a nearly flat outer region, and a large
#------hole at the centre. The function poses a risk for optimization algorithms, particularly hillclimbing
#------algorithms, to be trapped in one of its many local minima.
#------Recommended variable values are: a = 20, b = 0.2 and c = 2π.
def func1(x):
    total1 = 0
    total2 = 0
    a = 20
    b = 0.2
    term1 = 0
    term2 = 0
    c = 2*math.pi
    for i in range(len(x)):
        total1 += x[i]**2
        total2 += math.cos(c*x)
        term1 = -a*(math.exp(-b*math.sqrt(total1 / len(x))))
        term2 = -math.exp(total2 / len(x))
    return term1 + term2 + a + math.exp(1)


# --- MAIN ---------------------------------------------------------------------+

class Particle:
    def __init__(self, x0):
        self.position_i = []  # particle position
        self.velocity_i = []  # particle velocity
        self.pos_best_i = []  # best position individual
        self.err_best_i = -1  # best error individual
        self.err_i = -1  # error individual

        for i in range(0, num_dimensions):
            self.velocity_i.append(random.uniform(-1, 1))
            self.position_i.append(x0[i])

    # evaluate current fitness
    def evaluate(self, costFunc):
        self.err_i = costFunc(self.position_i)

        # check to see if the current position is an individual best
        if self.err_i < self.err_best_i or self.err_best_i == -1:
            self.pos_best_i = self.position_i.copy()
            self.err_best_i = self.err_i

    # update new particle velocity
    def update_velocity(self, pos_best_g):
        w = 0.5  # constant inertia weight (how much to weigh the previous velocity)
        c1 = 1  # cognative constant
        c2 = 2  # social constant

        for i in range(0, num_dimensions):
            r1 = random.random()
            r2 = random.random()

            vel_cognitive = c1 * r1 * (self.pos_best_i[i] - self.position_i[i])
            vel_social = c2 * r2 * (pos_best_g[i] - self.position_i[i])
            self.velocity_i[i] = w * self.velocity_i[i] + vel_cognitive + vel_social

    # update the particle position based off new velocity updates
    def update_position(self, bounds):
        for i in range(0, num_dimensions):
            self.position_i[i] = self.position_i[i] + self.velocity_i[i]

            # adjust maximum position if necessary
            if self.position_i[i] > bounds[i][1]:
                self.position_i[i] = bounds[i][1]

            # adjust minimum position if neseccary
            if self.position_i[i] < bounds[i][0]:
                self.position_i[i] = bounds[i][0]


class PSO():
    def __init__(self, costFunc, x0, bounds, num_particles, maxiter, verbose=False):
        global num_dimensions

        num_dimensions = len(x0)
        err_best_g = -1  # best error for group
        pos_best_g = []  # best position for group

        # establish the swarm
        swarm = []
        for i in range(0, num_particles):
            swarm.append(Particle(x0))

        # begin optimization loop
        i = 0
        while i < maxiter:
            if verbose: print(f'iter: {i:>4d}, best solution: {err_best_g:10.6f}')
            # cycle through particles in swarm and evaluate fitness
            for j in range(0, num_particles):
                swarm[j].evaluate(costFunc)

                # determine if current particle is the best (globally)
                if swarm[j].err_i < err_best_g or err_best_g == -1:
                    pos_best_g = list(swarm[j].position_i)
                    err_best_g = float(swarm[j].err_i)

            # cycle through swarm and update velocities and position
            for j in range(0, num_particles):
                swarm[j].update_velocity(pos_best_g)
                swarm[j].update_position(bounds)
            i += 1

        # print final results
        print('\nFINAL SOLUTION:')
        print(f'   > {pos_best_g}')
        print(f'   > {err_best_g}\n')


if __name__ == "__PSO__":
    main()

# --- RUN ----------------------------------------------------------------------+

initial = [5, 5]  # initial starting location [x1,x2...]
bounds = [(-10, 10), (-10, 10)]  # input bounds [(x1_min,x1_max),(x2_min,x2_max)...]
PSO(func1, initial, bounds, num_particles=15, maxiter=30, verbose=True)