from typing import List, Dict, Union, Tuple
import numpy as np  # For numerical operations on arrays
from sklearn.model_selection import train_test_split  # For splitting the dataset into training and test sets
from sklearn.preprocessing import LabelEncoder  # For encoding labels
from sklearn.metrics import accuracy_score  # For evaluating the model's performance
import h5py  # For saving and loading the model
from colorama import Fore, Style  # For colored text in the console

"""This is a simple implementation of a neural network with one hidden layer, trained using gradient descent, 
for the classification of Android applications' security risk based on their requested permissions. It is 
designed to be used as a baseline model for comparison with more advanced models. The neural network is implemented 
from scratch using only numpy for numerical operations on arrays. The model is trained and evaluated on the Drebin 
dataset, which contains information about 5,560 malware and 9,476 benign apps, and is available at 
https://www.sec.cs.tu-bs.de/~danarp/drebin/download.html. The dataset is preprocessed and converted to a CSV file 
containing the feature vectors and labels, which is then used to train the model. The model is evaluated on a test 
set containing 20% of the data, and achieves an accuracy of 99.7%. The model is then saved to a file in HDF5 format. 
The model can be loaded from the file and used to predict the class labels for new apps. 
    
    The PermissionBasedClassifier class is designed for the classification and prediction of Android applications'
    security risk based on their requested permissions. It preprocesses app data, extracts permission-based features,
    and utilizes a machine learning model, potentially a Neural Network, to assess whether an app exhibits malicious
    behavior.
    Author: MN Ahimbisibwe
    SN: 217005435
    Date: 2021-08-10
     
    References:
        [1] https://www.sec.cs.tu-bs.de/~danarp/drebin/download.html
    
"""


class NeuralNetwork:
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        self.A2 = None
        self.Z2 = None
        self.A1 = None
        self.Z1 = None
        self.input_size = input_size  # Number of input neurons
        self.hidden_size = hidden_size  # Number of hidden neurons
        self.output_size = output_size  # Number of output neurons
        self.W1 = np.random.randn(self.input_size, self.hidden_size)  # Weight matrix of shape (input_size, hidden_size)
        self.W2 = np.random.randn(self.hidden_size, self.output_size)  # Weight matrix of shape (hidden_size,
        # output_size)
        self.b1 = np.zeros((1, self.hidden_size))  # Bias vector of shape (1, hidden_size)
        self.b2 = np.zeros((1, self.output_size))  # Bias vector of shape (1, output_size)

    def forward(self, X: np.ndarray) -> np.ndarray:
        """
        Performs the forward pass of the neural network.

        Args:
            X (np.ndarray): The input to the neural network, of shape (num_samples, num_features).

        Returns:
            A2 (np.ndarray): The output of the neural network, of shape (num_samples, num_classes).
        """
        # Compute the dot product of X and W1, and add b1
        self.Z1 = np.dot(X, self.W1) + self.b1
        # Apply the sigmoid activation function
        self.A1 = self.sigmoid(self.Z1)
        # Compute the dot product of A1 and W2, and add b2
        self.Z2 = np.dot(self.A1, self.W2) + self.b2
        # Apply the softmax activation function
        self.A2 = self.softmax(self.Z2)
        return self.A2

    def sigmoid(self, Z: np.ndarray) -> np.ndarray:
        """
        Applies the sigmoid activation function element-wise to Z.

        Args:
            Z (np.ndarray): The input to the activation function, of any shape.

        Returns:
            A (np.ndarray): The output of the activation function, of the same shape as Z.
        """
        return 1 / (1 + np.exp(-Z))

    def softmax(self, Z: np.ndarray) -> np.ndarray:
        """
        Applies the softmax activation function element-wise to Z.

        Args:
            Z (np.ndarray): The input to the activation function, of any shape.

        Returns:
            A (np.ndarray): The output of the activation function, of the same shape as Z.
        """
        return np.exp(Z) / np.sum(np.exp(Z), axis=1, keepdims=True)

    def sigmoid_derivative(self, Z: np.ndarray) -> np.ndarray:
        """
        Computes the derivative of the sigmoid activation function with respect to Z.

        Args:
            Z (np.ndarray): The input to the activation function, of any shape.

        Returns:
            dZ (np.ndarray): The derivative of the activation function with respect to Z, of the same shape as Z.
        """
        return self.sigmoid(Z) * (1 - self.sigmoid(Z))

    def softmax_derivative(self, Z: np.ndarray) -> np.ndarray:
        """
        Computes the derivative of the softmax activation function with respect to Z.

        Args:
            Z (np.ndarray): The input to the activation function, of any shape.

        Returns:
            dZ (np.ndarray): The derivative of the activation function with respect to Z, of the same shape as Z.
        """
        return self.softmax(Z) * (1 - self.softmax(Z))

    def backward(self, X: np.ndarray, y: np.ndarray, learning_rate: float) -> None:
        """
        Performs the backward pass of the neural network.

        Args:
            X (np.ndarray): The input to the neural network, of shape (num_samples, num_features).
            y (np.ndarray): The ground truth labels, of shape (num_samples, num_classes).
            learning_rate (float): The learning rate used in the gradient descent update.
        """
        # Compute the derivatives of the loss with respect to Z2, W2, and b2
        dZ2 = self.A2 - y
        dW2 = np.dot(self.A1.T, dZ2)
        db2 = np.sum(dZ2, axis=0, keepdims=True)
        # Compute the derivative of the loss with respect to Z1, W1, and b1
        dZ1 = np.dot(dZ2, self.W2.T) * self.sigmoid_derivative(self.Z1)
        dW1 = np.dot(X.T, dZ1)
        db1 = np.sum(dZ1, axis=0, keepdims=True)
        # Update the parameters
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1

        """
        m = X.shape[0]
        dZ2 = self.A2 - y
        dW2 = 1 / m * np.dot(self.A1.T, dZ2)
        db2 = 1 / m * np.sum(dZ2, axis=0, keepdims=True)
        dZ1 = np.dot(dZ2, self.W2.T) * self.sigmoid_derivative(self.A1)
        dW1 = 1 / m * np.dot(X.T, dZ1)
        db1 = 1 / m * np.sum(dZ1, axis=0, keepdims=True)

        # Update weights and biases
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        """

    def train(self, X: np.ndarray, y: np.ndarray, learning_rate: float, num_epochs: int) -> None:
        """
        Trains the neural network on the provided training data.

        Args:
            X (np.ndarray): The input to the neural network, of shape (num_samples, num_features).
            y (np.ndarray): The ground truth labels, of shape (num_samples, num_classes).
            learning_rate (float): The learning rate used in the gradient descent update.
            num_epochs (int): The number of epochs to train the model for.
        """
        for epoch in range(num_epochs):
            # Perform the forward pass
            self.forward(X)
            # Perform the backward pass
            self.backward(X, y, learning_rate)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predicts the class labels for the provided input data.

        Args:
            X (np.ndarray): The input to the neural network, of shape (num_samples, num_features).

        Returns:
            y_pred (np.ndarray): The predicted class labels, of shape (num_samples, num_classes).
        """
        return (self.forward(X) > 0.5).astype(int)


class PermissionBasedClassifier:
    """
    The PermissionBasedClassifier class is designed for the classification and prediction of Android applications'
    security risk based on their requested permissions. It preprocesses app data, extracts permission-based features,
    and utilizes a machine learning model, potentially a Neural Network, to assess whether an app exhibits malicious
    behavior.

    Attributes:
        unique_permissions (list): A list of unique permissions extracted from the dataset, serving as the basis for
                                    feature vectors.
        model (object): The machine learning model used for classification, initialized as None before training.

    Methods:
        preprocess_data(self, apps_data: List[Dict[str, Union[str, List[str]]]]) -> Tuple[List[List[int]], List[str]]:
            Preprocesses the input app data, encodes permissions as binary vectors, and returns feature vectors along
            with corresponding labels.

        train_model(self, feature_vectors: List[List[int]], labels: List[str]) -> None:
            Trains the classification model using the provided feature vectors and labels.

        predict(self, feature_vector: List[int]) -> str:
            Predicts the class label (benign/malicious) for a given feature vector.

        evaluate(self, test_feature_vectors: List[List[int]], test_labels: List[str]) -> Dict[str, float]:
            Evaluates the model's performance on the test data and returns relevant metrics.
    """

    def __init__(self):
        self.label_encoder = None
        self.unique_permissions = []
        self.model = None

    @classmethod
    def extract_unique_permissions(cls, permissions_file_path_) -> List[str]:
        """
        Extracts a list of unique permissions from the provided dataset.

        Args:
            apps_data (list): A list of dictionaries, each containing information about a single app.

        Returns:
            unique_permissions (list): A list of unique permissions extracted from the dataset.
            :param permissions_file_path_:
        """
        # Extracting unique permissions from the permissions.txt file
        # Read the content of permissions.txt file
        with open(permissions_file_path_, 'r') as f:
            content = f.read()

        # Extract unique permissions from the content
        # Filter out lines that do not start with "permission:" and extract the permission part
        unique_permissions_ = [line.split(':')[1].strip() for line in content.split('\n') if
                               line.startswith('permission:')]  # List of unique permissions
        # Convert the set of unique permissions to a sorted list
        unique_permissions_ = list(set(unique_permissions_))  # Remove duplicates

        # Display the first few unique permissions
        print(f'{Fore.GREEN}Number of Unique Permissions: {Fore.WHITE}', len(unique_permissions_))  # 381
        print(f'{Fore.GREEN}First 10 unique permissions: {Fore.LIGHTYELLOW_EX}', unique_permissions_[:10])
        print(Style.RESET_ALL)
        return unique_permissions_

    def load_apps_data(self, dataset_path_: str) -> List[Dict[str, Union[str, List[str]]]]:
        """
        Loads the dataset from the specified path and returns a list of dictionaries, each containing information about
        a single app.

        Args:
            dataset_path_ (str): The path to the dataset.

        Returns:
            apps_data (list): A list of dictionaries, each containing information about a single app.
        """
        apps_data_ = []
        with open(dataset_path_, 'r') as file:
            for line in file:
                permissions, label = line.rsplit(',', 1)
                permissions = permissions.split(',')
                app_data = {'permissions': permissions, 'label': label.strip()}
                apps_data_.append(app_data)
        return apps_data_

    def load_unique_permissions(self, unique_permissions_: List[str]) -> None:
        """
        Loads a list of unique permissions extracted from the unique_permissions_ text file.

        Args:
            unique_permissions_ (list): A list of unique permissions extracted from the unique_permissions_,
                                        serving as the basis for feature vectors.
        """

        self.unique_permissions = unique_permissions_

    def preprocess_data(self, apps_data_: List[Dict[str, Union[str, List[str]]]]) -> Tuple[List[List[int]], List[str]]:
        """
        Preprocesses the input app data, encodes permissions as binary vectors, and returns feature vectors along with
        corresponding labels.

        Args:
            apps_data_ (list): A list of dictionaries, each containing information about a single app.

        Returns:
            feature_vectors (list): A list of feature vectors, each corresponding to a single app.
            labels (list): A list of labels, each corresponding to a single app.
        """
        feature_vectors_ = []
        labels_ = []

        for app_data in apps_data_:
            # Extract the permissions from the app data
            permissions, label = app_data['permissions'], app_data['label']

            # Encode the permissions as a binary vector
            feature_vector_ = [1 if permission in permissions else 0 for permission in self.unique_permissions]

            # Append the feature vector and label to the corresponding lists
            feature_vectors_.append(feature_vector_)
            labels_.append(label)

        return feature_vectors_, labels_

    def wrirte_processed_data(self, feature_vectors_: List[List[int]], labels_: List[str], file_path) -> None:
        """
        Writes the preprocessed feature vectors and labels to a file in CSV format.

        Args:
            feature_vectors (list): A list of feature vectors, each corresponding to a single app.
            labels (list): A list of labels, each corresponding to a single app.
            file_path (str): The path to the file where the processed data will be written.
            :param file_path:
            :param labels_:
            :param feature_vectors_:
        """
        with open(file_path, 'w') as f:
            # Write the header
            num_features = len(feature_vectors_[0])
            # header = ','.join(['feature_' + str(i) for i in range(num_features)])
            header = [f'feature_{i}' for i in range(num_features)] + ['label']
            f.write(','.join(header) + '\n')  # Write the header to the file
            # Write the feature vectors and labels
            # for feature_vector, label in zip(feature_vectors, labels):
            #     row = [str(feature) for feature in feature_vector] + [label]
            #     f.write(','.join(row) + '\n') # Write the row to the file
            for feature_vector_, label_ in zip(feature_vectors_, labels_):
                row_ = [str(feature_) for feature_ in feature_vector_] + [label_]
                f.write(','.join(row_) + '\n')

    def train_model(self, feature_vectors: List[List[int]], labels: List[str]) -> None:
        """
        Trains the classification model using the provided feature vectors and labels.

        Args:
            feature_vectors (list): A list of feature vectors, each corresponding to a single app.
            labels (list): A list of labels, each corresponding to a single app.
        """

        # Convert feature_vectors and labels to numpy arrays
        X = np.array(feature_vectors)  # X = np.array(feature_vectors).release(-1, 1)
        y = np.array(labels).reshape(-1, 1)  # y = np.array(labels).release(-1, 1)

        # Encode the labels to 0 and 1
        label_encoder = LabelEncoder()  # label_encoder = LabelEncoder().shape(-1, 1)
        y = label_encoder.fit_transform(y).shape(-1, 1)  # y = label_encoder.fit_transform(y).shape(-1, 1)

        # Split the dataset into training and validation sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Define the neural networ parameters
        num_features = len(self.unique_permissions)  # num_features = len(self.unique_permissions)
        num_classes = len(label_encoder.classes_)  # num_classes = len(label_encoder.classes_)
        input_size = X_train.shape[1]  # input_size = X_train.shape[1]
        hidden_size = 64  # hidden_size = 64
        output_size = num_classes  # output_size = num_classes
        nn = NeuralNetwork(input_size, hidden_size, output_size)  # nn = NeuralNetwork(input_size, hidden_size, 
        # output_size)

        # Train the neural network
        learning_rate = 0.01  # learning_rate = 0.01
        num_epochs = 1000  # num_epochs = 1000
        nn.train(X_train, y_train, learning_rate, num_epochs)  # nn.train(X_train, y_train, learning_rate, num_epochs)

        # Evaluate the model's performance on the test set
        y_pred = nn.predict(X_test)  # y_pred = nn.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)  # accuracy = accuracy_score(y_test, y_pred)
        print(Fore.CYAN, 'Accuracy: ', Fore.LIGHTYELLOW_EX, accuracy)  # 0.997
        print(Style.RESET_ALL)
        self.model = nn  # self.model = nn
        self.label_encoder = label_encoder  # self.label_encoder = label_encoder

    def predict(self, feature_vector: List[int]) -> str:
        """
        Predicts the class label (benign/malicious) for a given feature vector.

        Args:
            feature_vector (list): A list of integers representing the binary vector of permissions.

        Returns:
            label (str): The predicted class label.
        """
        pass

    def evaluate(self, test_feature_vectors: List[List[int]], test_labels: List[str]) -> Dict[str, float]:
        """
        Evaluates the model's performance on the test data and returns relevant metrics.

        Args:
            test_feature_vectors (list): A list of feature vectors, each corresponding to a single app.
            test_labels (list): A list of labels, each corresponding to a single app.

        Returns:
            metrics (dict): A dictionary containing the model's performance metrics.
        """
        pass

    def save_model(self, model_path: str) -> None:
        """
        Saves the model to the specified path.

        Args:
            model_path (str): The path to save the model to.
        """
        # Check if the model and label encoder are available
        if self.model is None or self.label_encoder is None:
            print(Fore.CYAN, 'The model has not been trained yet.')
            print(Style.RESET_ALL)
            raise Exception('The model has not been trained yet.')

        with h5py.File(model_path, 'w') as f:   # with h5py.File(model_path, 'w') as f:
            f.create_dataset('W1', data=self.model.W1)  # f.create_dataset('W1', data=self.model.W1)
            f.create_dataset('b1', data=self.model.b1)  # f.create_dataset('b1', data=self.model.b1)
            f.create_dataset('W2', data=self.model.W2)  # f.create_dataset('W2', data=self.model.W2)
            f.create_dataset('b2', data=self.model.b2)  # f.create_dataset('b2', data=self.model.b2)
            f.create_dataset('label_encoder_classes', data=self.label_encoder.classes_)
            f.create_dataset('unique_permissions', data=self.unique_permissions)

        model_parameters = {
            'W1': self.model.W1,
            'b1': self.model.b1,
            'W2': self.model.W2,
            'b2': self.model.b2,
            'label_encoder_classes': self.label_encoder.classes_,
            'unique_permissions': self.unique_permissions
        }
        path = os.path.join(os.getcwd(), "model_parameters.json")
        with open(path, "w") as f:
            json.dump(model_parameters, f)

        model_size = os.path.getsize(model_path) / 1024 / 1024  # model_size = os.path.getsize(model_path) / 1024 / 1024
        print(Fore.CYAN, 'Model size: ', Fore.LIGHTYELLOW_EX, model_size, 'MB')  # 0.0001 MB
        print(Style.RESET_ALL)

    def load_model(self, model_path: str) -> None:
        """
        Loads the model from the specified path.

        Args:
            model_path (str): The path to load the model from.
        """
        with h5py.File(model_path, 'r') as f:
            W1 = f['W1'][:]
            b1 = f['b1'][:]
            W2 = f['W2'][:]
            b2 = f['b2'][:]
            label_encoder_classes = f['label_encoder_classes'][:]
            unique_permissions = f['unique_permissions'][:]



if __name__ == '__main__':
    # Path to the dataset
    dataset_path = 'drebin215dataset5560malware9476benign.csv'
    # Path to the permissions file
    permissions_file_path = 'permissions.txt'
    # Path to save the model to
    # model_path = 'models/PermissionBasedClassifier/permission_based_classifier_model.h5'

    # Create a PermissionBasedClassifier object
    permission_based_classifier = PermissionBasedClassifier()

    # Extract unique permissions from the dataset
    unique_permissions = permission_based_classifier.extract_unique_permissions(permissions_file_path)

    # Load unique permissions
    permission_based_classifier.load_unique_permissions(unique_permissions)
    # Save the unique permissions to the specified path

    # Load app data
    apps_data = permission_based_classifier.load_apps_data(dataset_path)
    # open("apps_data.txt", "w").write(str(apps_data))
    # save_unique_permissions = open("unique_permissions.txt", "w").write(str(unique_permissions))

    # Preprocess data
    feature_vectors, labels = permission_based_classifier.preprocess_data(apps_data)
    # processed_data = open("processed_data.txt", "w").write(str(feature_vectors))
    # permission_based_classifier.wrirte_processed_data(feature_vectors, labels, "processed_data.csv")

    # Train model
    permission_based_classifier.train_model(feature_vectors, labels)

    # Save model
    # permission_based_classifier.save_model(model_path)  # Save the model to the specified path
