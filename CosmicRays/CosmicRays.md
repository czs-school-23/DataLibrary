# Question

Provided a point cloud from an astrophysical simulation where each point contains a data vector describing
various astrophysical local quantities (e.g., mass, magnetic field intensity, etc...), we wish to predict
the slope of the local cosmic ray power spectrum, or alternatively the entire cosmic ray power spectrum.

We therefore have a difficult version of the problem: predicting the cosmic ray power spectrum,
and a simple version: predicting the slope of the cosmic ray power spectrum.

# Dataset

Our input is an unordered data table of rank 4. Our output depends on whether we are trying to predict the
full power spectrum or only the slope. In the simple case, the output is a floating-point number, while in
the difficult case, the output is a 1D array.

# Current status

## Slope Regression

### Random Forest Sampling
TBD...
### XGBoost
TBD...
### Multi-Layer Perceptron

The MLP architecture consists of two fully-connected ("dense") layers, each followed by
a sigmoid nonlinear activation function. The first dense layer expands the 4-channel input
to 100 output channels, while the second dense layer compresses the 100-channel latent space to 
a single-channel output.

The data are normalized prior to being fed to the neural network to stabilize the gradients. Our
normalization scheme involves taking the base-10 logarithm of the full data matrix, and then
normalizing each of the four data columns such that its minimum is $0$ and its maximum is $1$.
This normalization is chosen so that the sigmoid activations do not lead to vanishing gradients.

An **important** drawback of the DataLoader wrapper in PyTorch was noted during the training of the
MLP. DataLoader sequentially loads in each item within a batch before passing the batch to the neural
network, which can lead to significant overhead when the batch size is large and the item size is small
(as is the case when each item is a $1$x$4$ tensor and our selected batch size is $2048$). We circumvented
this by writing our own training loop without the PyTorch wrappers.

After training the network on points from a single file (70-30 split of training and validation) for
1000 epochs, we achieve ~90% accuracy in slope prediction.

![The loss curves for the validation and training data over 1000 epochs.](./pictures/loss_curve.pdf)

![The residuals of the slope predictions. Error tends to be <10%.](./pictures/slope_residuals.pdf)

**Next Step**: Each regression machine should be used to perform symbolic regression, and thus 
create a rule for extrapolating slope beyond the provided range

**Possible issue**: This network was only trained on data from a single file, representing a single
time-slice of a galaxy's evolution. Will it generalize well to later time-slices? What about other
types of simulations?

## Power Spectrum Recovery

### Convolutional Neural Network

![True and predicted cosmic ray slopes from the trained CNN.](./pictures/conv_pred.pdf)

# Potential method

To solve the *simple* problem, we made three independent benchmark regression solutions:
1. Random Forest Sampling
2. XGBoost
3. Multi-Layer Perceptron

Meanwhile, we have also approached the *difficult* problem using a convolutional neural network.