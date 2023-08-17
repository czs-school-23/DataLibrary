# Question

## Big Question

Is there a way to predict solar flares?
Can we find evolution law from one time to another?

## What is your Scientific motivation?


## What are some of the limitations you face in this problem? For example, is it too slow right now? Is it very tedious to iterate through different configuration?

A lot of unobserved dynamics that affect the prediction accuracy.

## Is there some criterion a solution has to fulfill? For example, it has to be able to process n examples (throughput), or it has to be accurate down to some precision limit.

Any qualitative prediction would be great.

## Is uncertainty important?

Not really at this stage.

## Is there some smoothness condition you think would matter?

Not really

## How do we validate the accuracy

Autoencoding efficieny

# Dataset

## How much data do you have for training? Hundreds of GB? MB? or no data at all?

Raw data is 6TB. Image time series on a disk.

Active region data is also available. Preprocessed data is deprojected and cleaned.

## What's the dimension of your input and output? Is it constant or variable?

Variable size images. Larger image is ~2000x 700. Smaller image is about 400x400.

Output is the same dimension as the input.

## Do you expect the underlying process to be stochastic?

Somewhat stochastic.

## How many data channels you have?

3D vector of B field. Dopplergram (line of sight velocity). Continuum intensity (brightness). Magnetogram (line of sight magnetic field).

## Provide a short example to access and construct the test problem.

# Current status

1. Tried transformer, classify whethere there is a flare or not.
2. Tried LSTM, unclear whether it is necessary.

# Potential method

## Task

1. Predict the next time step.

## Suggest methods and why they might help.

1. Maybe combining information from AIA and HMI will help?
2. Neural SDE

## Brief list of tasks for building the network for beating the benchmark/production

## failure mode
