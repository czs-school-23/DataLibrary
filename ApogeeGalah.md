# Question

## Big Question

Can we generate GALAH spectra using APOGEE

## What is your Scientific motivation?

There are APOGEE (near IR) spectra and GALAH (optical). APORGEE does not give heavy element abundance because of weak lines and unknown lines, but signal to noise and labels very good.
GALAH is better for heavy element because strong numerous lines, however it has lower signal-to-noise ratio. Label are limited because of human resource reason.

TL;dr GALAH label is not usable and APOGEE label is not complete. It would be great if we can use both APOGEE and GALAH to produce better label.

Label being element abundance.


## What are some of the limitations you face in this problem? For example, is it too slow right now? Is it very tedious to iterate through different configuration?

## Is there some criterion a solution has to fulfill? For example, it has to be able to process n examples (throughput), or it has to be accurate down to some precision limit.

Having label for APOGEE itself would be great.

## Is uncertainty important?

## Is there some smoothness condition you think would matter?

## How do we validate the accuracy

1. Does it match the GALAH spectra? Particular for lines
2. Does label matches.

# Dataset

## How much data do you have for training? Hundreds of GB? MB? or no data at all?

Maximum 30000 spectra because of cross matching.
15000 Giants and 15000 dwarfs.

## What's the dimension of your input and output? Is it constant or variable?

8000 points spectra in APOGEE, and ~10000 points in GALAH. Same reolsution.

There are gaps in the spectra of both of them.

## Do you expect the underlying process to be stochastic?

In principle yes, but in principle no. But it shouldn't matter.

## How many data channels you have?

2.

## Provide a short example to access and construct the test problem.



# Current status

There is no APOGEE to GALAH leg, so anything that match GALAh, hence can be used to generate label is great.

# Potential method

Suggest methods and why they might help.

Brief list of tasks for building the network for beating the benchmark/production

failure mode

