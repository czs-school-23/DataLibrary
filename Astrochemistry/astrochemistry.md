# Question

## Big Question

Want to replace astrochemistry simulation

## What is your Scientific motivation?

Simulation is well known, but it is slow

## What are some of the limitations you face in this problem? For example, is it too slow right now? Is it very tedious to iterate through different configuration?

## Is there some criterion a solution has to fulfill? For example, it has to be able to process n examples (throughput), or it has to be accurate down to some precision limit.

Need stability, but accuracy requirement is limited by experiment anyway, which is about like 15%

## Is uncertainty important?

Not quite.

## Is there some smoothness condition you think would matter?

## How do we validate the accuracy

Check against solver.

# Dataset

## How much data do you have for training? Hundreds of GB? MB? or no data at all?

Can generate as much as possible

## What's the dimension of your input and output? Is it constant or variable?

16 chemical species (molecular), 20 reactions, 1 temperature

16*16 matrix, only ~20 non-zero

## Do you expect the underlying process to be stochastic?

Probably not

## How many data channels you have?

16 chemical species (molecular), 20 reactions, 1 temperature

16*16 matrix, only ~20 non-zero 

## Provide a short example to access and construct the test problem.

10k initialization. Randomly sampled in 6 dimensions like density
carbon, hydrogen and oxygen.

4-5k timesteps, chimical elements, and temperature.

5GB

# Current status

# Potential method

## Suggest methods and why they might help.

1. Neural ODE
2. Predictor-corrector

## Brief list of tasks for building the network for beating the benchmark/production

## failure mode
