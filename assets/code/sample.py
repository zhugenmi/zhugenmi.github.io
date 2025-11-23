import numpy as np
import tensorflow as tf

# 定义二次函数的系数
coefficient = np.array([[1.], [-10.], [25.]])

# 接下来，让我们定义参数 w，在 TensorFlow 中，你要用 tf.Variable() 来定义参数
w = tf.Variable(0, dtype=tf.float32)

# 然后我们定义损失函数
x = tf.constant(coefficient, dtype=tf.float32)

# 定义梯度下降优化器和训练操作
optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)

# 定义训练循环
for _ in range(1000):
    with tf.GradientTape() as tape:
        cost = x[0][0] * w ** 2 + x[1][0] * w + x[2][0]

    gradients = tape.gradient(cost, [w])
    optimizer.apply_gradients(zip(gradients, [w]))

# 打印更新后的参数 w 的值
print(w.numpy())