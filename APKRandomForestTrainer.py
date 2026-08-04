import os
import pickle
import json  # You are using json, but missing the import statement
from colorama import Fore

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics  # Missing import for metrics
from datetime import datetime  # Missing import for datetime

from APKManifestoExtractor import APKDetailsExtractor
from Tool import WarningCode


# You might need to install androguard: pip install androguard

class APKAnalyseWithRandomForest:
    def __init__(self, normal_apks_dir, malware_apks_dir):

        self.malware_apks_dir = malware_apks_dir
        self.normal_apks_dir = normal_apks_dir
        self.feature_extractor = None
        self.model = None
        self.unpack_apk = None
        self.apk_data_list = []

        self.mirror = load_permissions_from_file()

        self.f_measure = None
        self.precision = None
        self.recall = None
        self.accuracy = None

        self.date_created = None
        self.parent_name = None
        self.run()

    def return_unpack(self, apk_path):
        # Implement your feature extraction logic here using androguard or any other method
        # Return the extracted features as a numpy array
        pass

    def collect_data_from_normal_apks(self, apk_folder_path, is_malware=0):

        for root_dir, sub_dirs, apk_files in os.walk(apk_folder_path):
            for apk_filename in apk_files:
                try:
                    apk_full_path = os.path.join(root_dir, apk_filename)
                    if apk_filename.endswith(".apk"):
                        self.unpack_apk = APKDetailsExtractor(apk_full_path)
                        unpacked_apk_data = self.unpack_apk.extract()
                        if unpacked_apk_data is not None:
                            list_apk_feature_data = self.convert_apk_to_feature_data(unpacked_apk_data, is_malware)
                            self.apk_data_list.append(list_apk_feature_data)
                except Exception as e:
                    print(f"Failed processing {apk_filename}: {e}")

        # return apk_data_list

    def collect_data_from_malware_apks(self, apk_folder_path, is_malware=1):

        for root_dir, sub_dirs, apk_files in os.walk(apk_folder_path):
            for apk_filename in apk_files:
                try:
                    apk_full_path = os.path.join(root_dir, apk_filename)
                    if apk_filename.endswith(".apk"):
                        self.unpack_apk = APKDetailsExtractor(apk_full_path)
                        unpacked_apk_data = self.unpack_apk.extract()
                        if unpacked_apk_data is not None:
                            list_apk_feature_data = self.convert_apk_to_feature_data(unpacked_apk_data, is_malware)
                            self.apk_data_list.append(list_apk_feature_data)
                except Exception as e:
                    print(f"Failed processing {apk_filename}: {e}")

        # return apk_data_list
    """ """
    def train(self):
        data_flame = pd.DataFrame(columns=self.mirror)
        for i in range(0, len(self.apk_data_list)):
            data_flame.loc[i] = self.apk_data_list[i]
        feature = data_flame
        if 'ID' in feature.keys():  # Remove the ID column
            feature.drop(feature.columns[0], axis=1, inplace=True)
        feature.reset_index(drop=True, inplace=True)
        y = feature[['is_malware']]  # Labels
        X = feature.drop(axis=1, labels=['is_malware'])  # Features

        # X, y = self.prepare_data()

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize and train the Random Forest model
        random_forest = RandomForestClassifier(n_estimators=100, max_depth=50, oob_score=True)
        random_forest.fit(X_train, y_train.values.ravel())

        # Evaluate the model
        y_prediction = random_forest.predict(X_test)
        # Print accuracy, recall, precision, F-measure
        self.evaluate_model(y_test, y_prediction)
        self.model = random_forest
        self.parent_name = 'model'
        self.date_created = datetime.today().strftime('%Y-%m-%d')

        mdl_data = {"model": self.model,
                    "parent_date": self.parent_name,  # parent_date is a reserved keyword in Python
                    "date_created": self.date_created,  # date_created is a reserved keyword in Python
                    "accuracy": self.accuracy,
                    "recall": self.recall,
                    "precision": self.precision,
                    "f1": self.f_measure,  # f1 is a reserved keyword in Python
                    }
        pickle.dump(mdl_data, open('apk_hacking_model', 'wb'))

    def evaluate_model(self, y_test, y_prediction):
        self.accuracy = metrics.accuracy_score(y_test, y_prediction)
        self.recall = metrics.recall_score(y_test, y_prediction)
        self.precision = metrics.precision_score(y_test, y_prediction)
        self.f_measure = metrics.f1_score(y_test, y_prediction)

        print("Accuracy: {}".format(accuracy))
        print("Recall: {}".format(recall))
        print("Precision: {}".format(precision))
        print("F-Measure: {}".format(f_measure))

    def convert_apk_to_feature_data(self, apk, is_malware=WarningCode.SUCCESS.value):

        # Create a dictionary with default values set to 0 for each permission in mirror
        permission_mapping = dict((i, WarningCode.SUCCESS.value) for i in self.mirror)

        # Ensure there's a placeholder for permissions not in the mirror
        permission_mapping.setdefault("other_permission", WarningCode.SUCCESS.value)

        # Go through the APK permissions and update the dictionary
        for perm in apk["allowed_permissions"]:
            if perm in list(self.mirror):
                permission_mapping[perm] = WarningCode.PASS.value
            else:
                permission_mapping["other_permission"] += WarningCode.PASS.value

        # Attach additional data to the dictionary
        permission_mapping["num_of_permissions"] = len(apk["allowed_permissions"])

        if is_malware is not None:
            permission_mapping["is_malware"] = is_malware
        else:
            permission_mapping.pop("is_malware")

        # Convert the dictionary values to a list and return
        return list(permission_mapping.values())

    def identify_is_hacked(self, app_apk_dir, hacking_pretrained_model_dir):
        # If the model is not loaded, load it from the pretrained model file
        if self.model is None:
            # Load the pre-trained model and associated metrics
            model_load = pickle.load(open(hacking_pretrained_model_dir, 'rb'))
            self.model = model_load["model"]  # Load the pre-trained model from the pickle file
            self.accuracy = model_load["accuracy"]  # Load the accuracy metric
            self.recall = model_load["recall"]
            self.precision = model_load["precision"]
            self.f_measure = model_load["f1"]  # Load the F1-score metric from the pickle file

        # Calculate and save feature importance scores
        weights = {self.mirror[i]: weight for i, weight in enumerate(self.model.feature_importances_)}
        sorted_weights = dict(sorted(weights.items(), key=lambda item: item[1]))

        with open("model_stats.json", "w") as stats:
            json.dump(sorted_weights, stats, indent=4)

        # Extract APK data and prepare for prediction

        # Create an instance of APKDetailsExtractor
        apk_extractor = APKDetailsExtractor(app_apk_dir)

        # Extract APK data and prepare for prediction
        apk_data = apk_extractor.extract()  # Call the extract method
        list_of_data = self.convert_apk_to_feature_data(apk_data, is_malware=None)

        # Make a prediction using the loaded model
        result = self.model.predict([list_of_data])

        return result[0], apk_data

    def run(self):
        self.collect_data_from_malware_apks(self.malware_apks_dir)
        self.collect_data_from_normal_apks(self.normal_apks_dir)


def load_permissions_from_file():
    with open("permissions.txt", "r") as permissions_file:
        permissions = [line.strip() for line in permissions_file]
    return permissions


def detect_malicious_app(app_apk_to_analyse: str, results_destination_JSON: str, pre_trained_model):
    we_can_analyse_with = APKAnalyseWithRandomForest("android-malware", "normal_apks")  # If you need training again
    # pass both files
    hacking_model_path = f"{os.path.dirname(os.path.abspath(__file__))}" + pre_trained_model

    # Provide the APK file to check
    # app_apk_to_analyse = input("Enter the path to the APK file to analyze: ")

    if not app_apk_to_analyse.endswith(".apk"):
        raise Exception("Please provide an .apk file.")

    # Check if model should be re-trained
    if not os.path.isfile(hacking_model_path):
        malware_folder = "android-malware"
        normal_folder = "normal_apks"

        if os.path.isdir(malware_folder) and os.path.isdir(normal_folder):
            apk_info = we_can_analyse_with.train_model(malware_apks_folder_path=malware_folder,
                                                       normal_apks_folder_path=normal_folder)
        else:
            raise Exception("Malware and normal APK folders not found for training.")

    # Check if the model exists
    if os.path.exists(hacking_model_path):
        outcomes, apk_data = we_can_analyse_with.identify_is_hacked(app_apk_to_analyse, hacking_model_path)

        if outcomes == 1:
            print(Fore.YELLOW + "Analysed App" + Fore.RED + "{}', Status--> Malicious!".format(
                app_apk_to_analyse) + Fore.WHITE)
        else:
            print(Fore.YELLOW + "Analysed App" + Fore.GREEN + "'{}', Status-->Not Malicious.".format(
                app_apk_to_analyse) + Fore.WHITE)

        # Provide the destination JSON file if needed
        # results_destination_JSON = input("Enter the path to the destination JSON file (optional): ")

        if results_destination_JSON.endswith(".json"):
            outcomes = True if outcomes == 1 else False
            package_name = apk_data.get("package", "Unknown Package")  # Get the package name or use a default
            data_to_write = {package_name: outcomes}
            # data_to_write = {apk_data["package"]: outcomes}

            if os.path.isfile(results_destination_JSON) and os.stat(results_destination_JSON).st_size != 0:
                with open(results_destination_JSON) as json_file:
                    current_json_data = json.load(json_file)
                    current_json_data.update(data_to_write)
                    data_to_write = current_json_data

            with open(results_destination_JSON, 'w') as file_p:
                json.dump(data_to_write, file_p, indent=4)
            print(Fore.CYAN + "Data written to JSON file." + Fore.WHITE)

        else:
            print("Destination file provided was not a JSON file.")

    else:
        raise Exception("No model found. Please train the model.")


if __name__ == '__main__':
    detect_malicious_app("QR.apk", "model_stats.json", "\\apk_hacking_model\\apk_hacking_high.model")
