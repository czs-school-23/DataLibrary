import numpy as np

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import regularizers
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import tensorflow.keras.backend as K

tf.config.list_logical_devices()

dataset = np.load('database.npz')
N = dataset['input_data'].shape[0]
nparams = dataset['input_data'].shape[1]

#idx = np.arange(N)
#np.random.shuffle(idx)
#np.save('idx', idx)
idx = np.load('idx.npy')

train_end_idx = int(N*0.7)
val_end_idx = int(N*0.8)

X_train = dataset["input_data"][idx][:train_end_idx]
Y_train = dataset["output_data"][idx][:train_end_idx]

X_val = dataset["input_data"][idx][train_end_idx:val_end_idx]
Y_val = dataset["output_data"][idx][train_end_idx:val_end_idx]

X_test = dataset["input_data"][idx][val_end_idx:]
Y_test = dataset["output_data"][idx][val_end_idx:]
print('Training size: ', Y_train.shape)
print('Validation size: ', Y_val.shape)
print('Test size: ', Y_test.shape)


batch_size = 2048


train = tf.data.Dataset.from_tensor_slices((X_train, Y_train))
training_data = train.shuffle(X_val.shape[0]).batch(batch_size)

val = tf.data.Dataset.from_tensor_slices((X_val, Y_val))
validation_data = val.shuffle(X_val.shape[0]).batch(batch_size)

nlayers = 6
nnodes_mlp = [256,256, 256, 256,500,12]

input_layer = layers.Input(shape = nparams)#, batch_size = batch_size)

for i in range(nlayers):
    if type(nnodes_mlp) == int:
        nnodes = nnodes_mlp
    else:
        assert len(nnodes_mlp) == nlayers
        nnodes = nnodes_mlp[i]
    if i == 0:
        mlp = layers.Dense(nnodes, kernel_initializer = 'random_normal', 
                                   bias_initializer = 'Zeros', name = 'Dense_' + str(i))(input_layer)
    else:
        mlp = layers.Dense(nnodes, kernel_initializer = 'random_normal', 
                                   bias_initializer = 'Zeros', name = 'Dense_' + str(i))(mlp)
    if i < nlayers:
        mlp = layers.LeakyReLU(alpha = 0.1,name = 'LReLU_' + str(i))(mlp)

model = tf.keras.Model(inputs = [input_layer], outputs = [mlp])
model.summary()

@tf.function
def loss_fnc():
    def loss(y_true, y_pred):
        return K.mean(K.square(y_true - y_pred))
    return loss

opt = Adam(learning_rate = 1e-3)
model.compile(loss = 'mse',
                    optimizer = opt,
                    )

callbacks = [tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience = 10, restore_best_weights = True),
             tf.keras.callbacks.ReduceLROnPlateau(patience = 4, min_lr = 1e-7)
             
    ]

history = model.fit(training_data,
                  epochs = 20,
                  batch_size = batch_size,
                  validation_data = validation_data,
                  callbacks = callbacks,
                  shuffle = True, # shuffle the data in each batch
                  )

model.save('model')
np.savez('history', loss = history.history['loss'], lr = history.history['lr'], val_loss = history.history['val_loss'])

