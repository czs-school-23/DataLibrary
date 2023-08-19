from pysr import PySRRegressor
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

pd.set_option("display.max_rows", 10000)
pd.set_option("display.expand_frame_repr", True)
pd.set_option('display.max_colwidth', 3000)
pd.set_option('display.width', 10000)

Nsample = 10000

model = PySRRegressor(
    niterations=40,  # < Increase me for better results
    binary_operators=["+", "*"],
    unary_operators=[
        #"cos",
        "exp",
        #"sin",
        "inv(x) = 1/x",
        # ^ Custom operator (julia syntax)
    ],
    extra_sympy_mappings={"inv": lambda x: 1 / x},
    # ^ Define operator for SymPy as well
    loss="loss(prediction, target) = (prediction - target)^2",
    # ^ Custom loss function (julia syntax)
    progress = False,
)


dens   = np.load("sum-data-dens.npy")
radius = np.load("sum-data-radius.npy")
encr   = np.load("sum-data-encr.npy")
Babs   = np.load("sum-data-Babs.npy")
slope  = np.load("sum-data-slope.npy")


# randomly select some cells

# number of random selections
Ntries = 50

for i in range(Ntries):
    print(i)
    idx = np.random.choice(np.arange(dens.size), size=Nsample)
    #print(idx)
    X = np.vstack((dens[idx], radius[idx], encr[idx], Babs[idx])).T
    y = slope[idx]

    model.fit(X, y)
    with open('01-best-model-'+str(i).zfill(3)+'.txt', 'w') as f:
        print(model, file=f)
    with open('01-best-model-'+str(i).zfill(3)+'-latex.txt', 'w') as f:
        print(model.latex(), file=f)
    with open('01-best-model-'+str(i).zfill(3)+'-sympy.txt', 'w') as f:
        print(model.sympy(), file=f)

    fig, ax = plt.subplots()
    ax.scatter(y, model.predict(X), s=3)
    ax.set_xlabel("true slope")
    ax.set_ylabel("predicted slope")
    fig.savefig("01-test-true-vs-predict-"+str(i).zfill(3)+".pdf")
