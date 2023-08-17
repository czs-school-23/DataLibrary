# Question

## What is your Scientific motivation?

There is a bunch of 21cm simulations. Right now we are getting a lot of new data. We need to rerun the data analysis very frequently and rapidly.

## What are some of the limitations you face in this problem? For example, is it too slow right now? Is it very tedious to iterate through different configuration?

## Is there some criterion a solution has to fulfill? For example, it has to be able to process n examples (throughput), or it has to be accurate down to some precision limit.

## Is uncertainty important?

That would be nice to have uncertainty estimate.

## Is there some smoothness condition you think would matter?

# Dataset

## What's the dimension of your input and output? Is it constant or variable?

The input is astrophysical parameters, and the output are summary statistics, such as power spectrum.

## How much data do you have for training? Hundreds of GB? MB? or no data at all?

A million examples. About a couple GB

# Do you expect the underlying process to be stochastic?

Not really.

## How many data channels you have?

There are 9 input astrophysical parameters, and 6 groups of output (1998 of numbers).

Provide a short example to access and construct the test problem.

# Current status

## Current method benchmark.

Current emulator seems to work okay. The emulator is pretty big, so it would be nice to prune it.

# Potential method

## Task

1. Given emulator, compute the summary statistics, and then use the summary statistics to compute the likelihood.
2. Would be nice to have uncertainty estimate.
3. Would be nice to trim the network.
4. Robust against adverserial attack.

## Suggest methods and why they might help.

1. Residual connection should help the convolutional part.
2. Dropout can help with uncertainty estimate.
3. Add noise to summary statics/simulation to make it robust against adverserial attack.

## Brief list of tasks for building the network for beating the benchmark/production

## failure mode

