### Библиотеки
# Стандартные библиотеки
import random  # генерация случайных значений

# Сторонние библиотеки
import numpy as np  # работа с матрицами


def sigmoid(z):
    """Сигмоидальная функция активации"""
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_prime(z):
    """Производная сигмоидальной функции"""
    return sigmoid(z) * (1 - sigmoid(z))

""" ---Раздел описаний--- """
""" ---Описание класса Network--- """
class Network(object):
    """Класс для описания нейронной сети"""

    def __init__(self, sizes):
        """
        self - указатель на объект класса
        sizes – список размеров слоёв сети
        """
        self.num_layers = len(sizes) # Задаем количество слоев нейронной сети
        self.sizes = sizes # Задаем список размеров слоев нейронной сети
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]] # Задаем случайные начальные смещения
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])] # Задаем случайные начальные веса связей

    def feedforward(self, a):
        """Подсчёт выходных сигналов сети для входного вектора a"""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        """Стохастический градиентный спуск
            self - указатель на объект класса
            training_data - обучающая выборка
            epochs - количество эпох обучения
            mini_batch_size - размер подвыборки
            eta - скорость обучения
            test_data - тестирующая выборка
        """
        if test_data:
            test_data = list(test_data) # Создаем список объектов тестовой выборки
            n_test = len(test_data) # Вычисляем размер тестовой выборки
        else:
            n_test = 0

        training_data = list(training_data) # Создаем список объектов обучающей выборки
        n = len(training_data) # Вычисляем размер обучающей выборки

        for j in range(epochs): # Цикл по эпохам
            random.shuffle(training_data) # Перемешивание элементов обучающей выборки
            mini_batches = [
                training_data[k:k + mini_batch_size]
                for k in range(0, n, mini_batch_size) # Создание подвыборки
            ]
            for mini_batch in mini_batches: # Цикл по подвыборкам
                self.update_mini_batch(mini_batch, eta) # Один шаг градиентного спуска
            # if test_data:
                # print(f"Epoch {j}: {self.evaluate(test_data)} / {n_test}") # Смотрим прогресс обучения
            # else:
                # print(f"Epoch {j} complete!") # Если тестовых данных нет, то выводится сообщения успеха завершения эпохи

    def update_mini_batch(self, mini_batch, eta):
        """Один шаг градиентного спуска
            self - указатель на объект класса
            mini_batch - подвыборка
            eta - скорость обучения
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases] # Список градиентов dC/db для каждого слоя (первоначально заполняются нулями)
        nabla_w = [np.zeros(w.shape) for w in self.weights]  # Список градиентов dC/dw для каждого слоя (первоначально заполняются нулями)

        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y) # Послойно вычисляем градиенты dC/db и dC/dw для текущего прецедента (x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)] # Суммируем градиенты dC/db для различных прецедентов текущей подвыборки
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)] # Суммируем градиенты dC/dw для различных прецедентов текущей подвыборки

        self.weights = [w - (eta / len(mini_batch)) * nw
                        for w, nw in zip(self.weights, nabla_w)] # Обновляем все веса w нейронной сети
        self.biases = [b - (eta / len(mini_batch)) * nb
                       for b, nb in zip(self.biases, nabla_b)] # Обновляем все смещения b нейронной сети

    def backprop(self, x, y):
        """Алгоритм обратного распространения ошибки
            self - указатель на объект класса
            x - вектор входных сигналов
            y - ожидаемый вектор выходных сигналов
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases] # Список градиентов dC/db для каждого слоя (первоначально заполняются нулями)
        nabla_w = [np.zeros(w.shape) for w in self.weights] # Список градиентов dC/dw для каждого слоя (первоначально заполняются нулями)

        # Определенеи переменных 
        activation = x # Выходные сигналы слоя (первоначально соответствует выходным сигналам 1-го слоя или входным сигналам сети)
        activations = [x] # Список выходных сигналов по всем слоям (первоначально содержит только выходные сигналы 1-го слоя)
        zs = [] # Список активационных потенциалов по всем слоям (первоначально пуст)

        # Прямое распространение
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b # Считаем активационные потенциалы текущего слоя
            zs.append(z)  # Добавляем элемент (активационные потенциалы слоя) в конец списка
            activation = sigmoid(z)  # Считаем выходные сигналы текущего слоя, применяя сигмоидальную функцию активации к активационным потенциалам слоя
            activations.append(activation) # Добавляем элемент (выходные сигналы слоя) в конец списка

        # Обратное распространение
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1]) # Cчитаем меру влияния нейронов выходного слоя L на величину ошибки (BP1)
        nabla_b[-1] = delta # Градиент dC/db для слоя L (BP3)
        nabla_w[-1] = np.dot(delta, activations[-2].transpose()) # Градиент dC/dw для слоя L (BP4)

        for l in range(2, self.num_layers):
            z = zs[-l] # Активационные потенциалы l-го слоя (двигаемся по списку справа налево)
            sp = sigmoid_prime(z) # Считаем сигмоидальную функцию от активационных потенциалов l-го слоя
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp  # Считаем меру влияния нейронов l-го слоя на величину ошибки (BP2)
            nabla_b[-l] = delta # Градиент dC/db для l-го слоя (BP3)
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose()) # Градиент dC/dw для l-го слоя (BP4)

        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """Оценка прогресса на тестовых данных"""
        test_results = [(np.argmax(self.feedforward(x)), y) for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        """Вычисление частных производных стоимостной функции по выходным сигналам последнего слоя"""
        return (output_activations - y)
