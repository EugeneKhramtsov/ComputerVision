import numpy as np
import matplotlib.pyplot as plt
import random

def random_swaps(arr, changes):
    result = arr.copy()

    for _ in range(changes):
        i, j = random.sample(range(len(result)), 2)
        result[i], result[j] = result[j], result[i]

    return result

def input_data(swaps = 0):
    two = [0,1,1,1,0,
           1,0,0,0,1,
           0,0,0,0,1,
           0,0,0,1,0,
           0,0,1,0,0,
           0,1,0,0,0,
           1,1,1,1,1]
    three = [0,1,1,1,0,
             1,0,0,0,1,
             0,0,0,0,1,
             0,1,1,1,0,
             0,0,0,0,1,
             1,0,0,0,1,
             0,1,1,1,0]
    four = [0,0,1,1,0,
            0,1,0,1,0,
            1,0,0,1,0,
            1,1,1,1,1,
            0,0,0,1,0,
            0,0,0,1,0,
            0,0,0,1,0]
    seven = [1,1,1,1,1,
             0,0,0,0,1,
             0,0,0,1,0,
             0,0,1,0,0,
             0,0,1,0,0,
             0,0,1,0,0,
             0,0,1,0,0]
    eight = [0,1,1,1,0,
             1,0,0,0,1,
             1,0,0,0,1,
             0,1,1,1,0,
             1,0,0,0,1,
             1,0,0,0,1,
             0,1,1,1,0]
    nine = [0,1,1,1,0,
            1,0,0,0,1,
            1,0,0,0,1,
            0,1,1,1,1,
            0,0,0,0,1,
            1,0,0,0,1,
            0,1,1,1,0]

    two = random_swaps(two, swaps)
    three = random_swaps(three, swaps)
    four = random_swaps(four, swaps)
    seven = random_swaps(seven, swaps)
    eight = random_swaps(eight, swaps)
    nine = random_swaps(nine, swaps)

    plt.subplot(1, 6, 1)
    plt.imshow(np.array(two).reshape((7, 5)), cmap='YlGn')
    plt.subplot(1, 6, 2)
    plt.imshow(np.array(three).reshape((7, 5)), cmap='YlGn')
    plt.subplot(1, 6, 3)
    plt.imshow(np.array(four).reshape((7, 5)), cmap='YlGn')
    plt.subplot(1, 6, 4)
    plt.imshow(np.array(seven).reshape((7, 5)), cmap='YlGn')
    plt.subplot(1, 6, 5)
    plt.imshow(np.array(eight).reshape((7, 5)), cmap='YlGn')
    plt.subplot(1, 6, 6)
    plt.imshow(np.array(nine).reshape((7, 5)), cmap='YlGn')

    plt.show()

    x = [np.array(two).reshape(1, 35),
         np.array(three).reshape(1, 35),
         np.array(four).reshape(1, 35),
         np.array(seven).reshape(1, 35),
         np.array(eight).reshape(1, 35),
         np.array(nine).reshape(1, 35)]

    return x

def output_data():
    out_numbers = [[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]]
    y = np.array(out_numbers)

    return y

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def forward_propagation(x, w1, w2):

    z1 = x.dot(w1)
    a1 = sigmoid(z1)

    z2 = a1.dot(w2)
    a2 = sigmoid(z2)

    return a2

def generate_weights(x, y):
    l = []
    for i in range(x * y):
        l.append(np.random.randn())

    return np.array(l).reshape(x, y)

def loss_func(output, target):
    return np.sum(np.square(output - target)) / len(output)

def back_propagation(x, y, w1, w2, alpha):
    z1 = x.dot(w1)
    a1 = sigmoid(z1)

    z2 = a1.dot(w2)
    a2 = sigmoid(z2)

    d2 = (a2 - y)
    d1 = np.multiply(w2.dot(d2.transpose()).transpose(), np.multiply(a1, 1 - a1))

    w1_adjust = x.transpose().dot(d1)
    w2_adjust = a1.transpose().dot(d2)

    w1 = w1 - (alpha * w1_adjust)
    w2 = w2 - (alpha * w2_adjust)

    return w1, w2

def train(x, y, w1, w2, alpha = 0.01, epochs = 10):
    accuracy = []
    loss = []

    for j in range(epochs):
        l = []
        for i in range(len(x)):
            output = forward_propagation(x[i], w1, w2)
            l.append(loss_func(output, y[i]))
            w1, w2 = back_propagation(x[i], y[i], w1, w2, alpha)

        accuracy.append((1 - sum(l) / len(x)) * 100)
        loss.append(sum(l) / len(x))
        print("epochs:", j + 1, ", accuracy:", accuracy[j], ", loss:", loss[j])

    return accuracy, loss, w1, w2

def predict(x, w1, w2, label = None):
    numbers_titles = ["TWO", "THREE", "FOUR", "SEVEN", "EIGHT", "NINE"]

    out = forward_propagation(x, w1, w2)
    k = int(np.argmax(out[0]))
    conf = out[0][k] * 100

    print(f'Input: {label}, Identified as: {numbers_titles[k]}, Confusion: {conf}%')

    plt.figure()
    plt.imshow(x.reshape((7, 5)), cmap='YlGn')
    plt.title(f'Identified as: {numbers_titles[k]}, Confusion: {conf}%')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return

input_layer = 35
hidden_layer = 5
output_layer = 6
print("NN architecture: ")
print("Input layer: ", input_layer)
print("Hidden layer: ", hidden_layer)
print("Output layer: ", output_layer)

x = input_data()
y = output_data()
print("Input data:\n", x)
print("Output data:\n", y)

w1 = generate_weights(input_layer, hidden_layer)
w2 = generate_weights(hidden_layer, output_layer)
print("w1 = ", w1)
print("w2 = ", w2)

acc, loss, w1, w2 = train(x, y, w1, w2, alpha = 0.2, epochs = 200)
print("Trained w1 = ", w1)
print("Trained w2 = ", w2)

plt.plot(acc)
plt.ylabel('Accuracy')
plt.xlabel('Epochs')
plt.show()

plt.plot(loss)
plt.ylabel('Loss')
plt.xlabel('Epochs')
plt.show()

number_of_random_distortions = 2
x_pred = input_data(number_of_random_distortions)

print("Number TWO identification:")
predict(x_pred[0], w1, w2, "Two")
print("Number THREE identification:")
predict(x_pred[1], w1, w2, "THREE")
print("Number FOUR identification:")
predict(x_pred[2], w1, w2, "FOUR")
print("Number SEVEN identification:")
predict(x_pred[3], w1, w2, "SEVEN")
print("Number EIGHT identification:")
predict(x_pred[4], w1, w2, "EIGHT")
print("Number NINE identification:")
predict(x_pred[5], w1, w2, "NINE")

