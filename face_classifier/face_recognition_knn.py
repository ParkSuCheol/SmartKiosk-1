"""
This is an example of using the k-nearest-neighbors (KNN) algorithm for face recognition.

When should I use this example?
This example is useful when you wish to recognize a large set of known people,
and make a prediction for an unknown person in a feasible computation time.

Algorithm Description:
The knn classifier is first trained on a set of labeled (known) faces and can then predict the person
in an unknown image by finding the k most similar faces (images with closet face-features under euclidean distance)
in its training set, and performing a majority vote (possibly weighted) on their label.

For example, if k=3, and the three closest face images to the given image in the training set are one image of Biden
and two images of Obama, The result would be 'Obama'.

* This implementation uses a weighted vote, such that the votes of closer-neighbors are weighted more heavily.

Usage:

1. Prepare a set of images of the known people you want to recognize. Organize the images in a single directory
   with a sub-directory for each known person.

2. Then, call the 'train' function with the appropriate parameters. Make sure to pass in the 'model_save_path' if you
   want to save the model to disk so you can re-use the model without having to re-train it.

3. Call 'predict' and pass in your trained model to recognize the people in an unknown image.

NOTE: This example requires scikit-learn to be installed! You can install it with pip:

$ pip3 install scikit-learn

"""

import math
from pickle import FALSE
from sklearn import neighbors
import os
import os.path
import pickle
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import pandas as pd
from numpy import asarray, savetxt, loadtxt
import numpy as np
import shutil


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def train(train_dir, model_save_path="trained_knn_model.csv", n_neighbors=1, knn_algo='ball_tree', verbose=False):
    """
    Trains a k-nearest neighbors classifier for face recognition.

    :param train_dir: directory that contains a sub-directory for each known person, with its name.

     (View in source code to see train_dir example tree structure)

     Structure:
        <train_dir>/
        ├── <person1>/
        │   ├── <somename1>.jpeg
        │   ├── <somename2>.jpeg
        │   ├── ...
        ├── <person2>/
        │   ├── <somename1>.jpeg
        │   └── <somename2>.jpeg
        └── ...

    :param model_save_path: (optional) path to save model on disk
    :param n_neighbors: (optional) number of neighbors to weigh in classification. Chosen automatically if not specified
    :param knn_algo: (optional) underlying data structure to support knn.default is ball_tree
    :param verbose: verbosity of training
    :return: returns knn classifier that was trained on the given data.
    """
    # X = []
    # y = []
<<<<<<< HEAD
    X = loadtxt('C:/Users/multicampus/Desktop/lastpjt/s03p31b107/face_classifier/output2.csv', delimiter=',').tolist()
    y = loadtxt('C:/Users/multicampus/Desktop/lastpjt/s03p31b107/face_classifier/output3.csv', dtype=str).tolist()
=======
    X = loadtxt(base_path + "output2.csv", delimiter=',').tolist()
    y = loadtxt(base_path + "output3.csv", dtype=str).tolist()
>>>>>>> 86820ee01195305353fc89748218dd26abd12d69

    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                pass
            else:
                # Add face encoding for current image to the training set
                X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)

<<<<<<< HEAD
    shutil.rmtree("C:/Users/multicampus/Desktop/lastpjt/s03p31b107/face_classifier/knn_examples/train")
    os.mkdir("C:/Users/multicampus/Desktop/lastpjt/s03p31b107/face_classifier/knn_examples/train")
=======
    shutil.rmtree(base_path + "knn_examples/train")
    os.mkdir(base_path + "knn_examples/train")
>>>>>>> 86820ee01195305353fc89748218dd26abd12d69
    
    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))

    pointX = asarray(X)
    d = np.array(y)
    pointY = d.reshape(d.shape[0], -1)

    savetxt(base_path + "output2.csv", pointX, delimiter=',')
    savetxt(base_path + "output3.csv", pointY, fmt='%s')

    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)
    
    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf


def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.4):
    """
    Recognizes faces in given image using a trained KNN classifier

    :param X_img_path: path to image to be recognized
    :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
    :param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
    :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
           of mis-classifying an unknown person as a known one.
    :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
        For faces of unrecognized persons, the name 'unknown' will be returned.
    """
    if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("Invalid image path: {}".format(X_img_path))

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]


if __name__ == "__main__":
    base_path = "C:/Users/multicampus/Desktop/project/pjt3/s03p31b107_3/face_classifier/"
    flag = False
    # STEP 1: Train the KNN classifier and save it to disk
    # Once the model is trained and saved, you can skip this step next time.
<<<<<<< HEAD
    classifier = train("C:/Users/multicampus/Desktop/lastpjt/s03p31b107/face_classifier/knn_examples/train", model_save_path="trained_knn_model.csv", n_neighbors=1)

    # STEP 2: Using the trained classifier, make predictions for unknown images
    for image_file in os.listdir("C:/Users/multicampus/Desktop/lastpjt/s03p31b107/face_classifier/knn_examples/test"):
        full_file_path = os.path.join("C:/Users/multicampus/Desktop/lastpjt/s03p31b107/face_classifier/knn_examples/test", image_file)
=======
    classifier = train(base_path + "knn_examples/train", model_save_path=base_path + "trained_knn_model.csv", n_neighbors=1)

    # STEP 2: Using the trained classifier, make predictions for unknown images
    for image_file in os.listdir(base_path + "knn_examples/test"):
        full_file_path = os.path.join(base_path + "knn_examples/test", image_file)
>>>>>>> 86820ee01195305353fc89748218dd26abd12d69

        # Find all people in the image using a trained classifier model
        # Note: You can pass in either a classifier file name or a classifier model instance
        predictions = predict(full_file_path, model_path=base_path + "trained_knn_model.csv")

        # Print results on the console
        for name, (top, right, bottom, left) in predictions:
            print("{}".format(name))
            if name != "unknown":
                shutil.rmtree(base_path + "knn_examples/test")
                os.mkdir(base_path + "knn_examples/test")
                flag = True
                break
        if flag:
            break

