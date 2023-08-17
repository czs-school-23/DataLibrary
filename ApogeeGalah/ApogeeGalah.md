# Question

## Big Question

Can we generate GALAH spectra using APOGEE?

## What is your Scientific motivation?

There are APOGEE (near IR) spectra and GALAH (optical). APORGEE does not give heavy element abundance because of weak lines and unknown lines, but signal to noise and labels in other elements very good.
GALAH is better for heavy element because strong numerous heavy element lines, however it has lower signal-to-noise ratio, and label qualtiy is limited because of human resource reason.PI.jl/stable/configuration/

TL;dr GALAH label is not usable and APOGEE label is not complete. It would be great if we can use both APOGEE and GALAH to produce better label.

Label being heavy element abundance.


## What are some of the limitations you face in this problem? For example, is it too slow right now? Is it very tedious to iterate through different configuration?

## Is there some criterion a solution has to fulfill? For example, it has to be able to process n examples (throughput), or it has to be accurate down to some precision limit.

1. Having any heavy element labels for APOGEE itself would be great.
2. Synthesizing any lines in the GALAH spectral region from just an APOGEE spectrum would be great.
3. Synthesizing a full GALAH style spectrum is top level goal.

## Is uncertainty important?

If we are talking flux uncertainties, then it would be good if flux uncertainty around key spectral lines is pretty small (err in flux of GALAH style spectrum ~ 0.01)

## Is there some smoothness condition you think would matter?

## How do we validate the accuracy

1. Does it match the GALAH spectra? Particular for lines
2. Does label matches. (not as important--labels honestly should be ignored in my opinion because they are often unreliable even in best quality sample)

# Dataset

## How much data do you have for training? Hundreds of GB? MB? or no data at all?

Maximum 30000 spectra because of cross matching.
15000 Giants and 15000 dwarfs.

10 to 20 GB approx.

## What's the dimension of your input and output? Is it constant or variable?

8000 points spectra in APOGEE, and ~12000 points in GALAH. Same reolsution.

There are gaps in the spectra of both of them.

## Do you expect the underlying process to be stochastic?

In principle yes, but in principle no. But it shouldn't matter.

If two stars are same temperature, same logg, same chemical composition (metallicity, Mg, Si, Ce, etc. etc.), then spectra should be IDENTICAL!

## How many data channels you have?

2.

## Provide a short example to access and construct the test problem.


# Current status

There is no APOGEE to GALAH leg, so anything that match GALAh, hence can be used to generate label is great.

# Potential method

## Suggest methods and why they might help.

Proposal 1
Try a convnet for projecting both spectra to an embedding space.
Diffusion model for conditional generation.

Proposal 2
Convnet decode from one to another?

## Brief list of tasks for building the network for beating the benchmark/production

1. Start with zoom-in on a couple of lines. (Don't need to deal with long range correlation)
   1. Cut off part of the GALAH target
   2. Maybe downsample the APOGEE.
2. Good to check null case as well.
3. Generalize to large part of spectra.

## failure mode

??
