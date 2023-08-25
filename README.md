# MovementClassification
A desktop app that will differentiate between running and jumping through a phone's acceleration data. 
![gui3](https://github.com/D-Joseph/MovementClassification/assets/67702022/4f586a73-e98d-4fb5-ab76-58e13daab82c)

# How To Use
To use the classifier:
1. Download the Phyphox mobile app and conduct an "Acceleration (without g)" experiment
2. Export the generated CSV that contains the accelerometer data and timestamps, and feed it into the desktop app
3. The model will perform necessary calculations and predict what the user was doing per 5-second interval
4. The user can then save a labelled version of the CSV to their computer


# How It Was Developed
## Data Collection
The data for this project was collected using the Phyphox mobile application. For this step, we looked to collect sufficient diverse data for the model to be trained and tested. To achieve this, the group chose different positions on the body to keep the phone during the collection process across both walking and jumping. The decided placements were holding the phone in the right hand with the right arm extended down, keeping the phone in the right jacket pocket, and keeping the phone in the front right pant pocket. Each group member was tasked with collecting 5 minutes of data per action per position using the 'Acceleration (without g)' experiment on Phyphox. The collected data was then exported into the '/Data' folder.
## Data Storing
Once the raw experiment data was collected and stored within the repository, the next task was to segment it into 5-second windows and store it in an HDF5 file.

Firstly, each member's data was read into two separate Pandas DataFrames, one for walking data and another for jumping. To ensure that the dataset was balanced, the number of rows for each file was limited to the length of the smallest CSV. Doing so guarantees that the data that will train/test the model represents the same amount of time for each action, placement, and user. The data also needed to be segmented into 5-second windows, which at the 100Hz collection frequency of the iPhone, represented 500 records. Thus, to ensure that there would be no overlap with the segments the length of the smallest CSV was rounded down to the nearest multiple of 500. Without this step, the group would either have to segment the individual data files first before concatenating them into a bigger DataFrame, or run the risk of having windows that cross files.

Two new DataFrames were then created which concatenated the individual walking and jumping data respectively. A new column, Label, was added to both to classify the data, and a value of 0 was assigned to all walking records and 1 for all jumping records. Finally, these two DataFrames were concatenated into a frame that contained all labelled, collected data.

With one DataFrame, allData, containing all of the data, the group then performed the segmentation. As mentioned before, the 5-second segments were created as non-overlapping groups of 500 rows of data to avoid data leakage. First, the required number of segments was calculated by dividing the length of the data by 500. Then, iterating for the number of segments, indices that were 500 apart were calculated and used to splice allData. The splices were then appended to an array that stored the individual segments. It should be noted that at this step, the group also separated the labels from the data by specifying the desired columns during the splice. This created a relationship where there was one label for every 500-row 2D array, instead of one label per row. Doing so saved some work later in the project, specifically after feature extraction.

The next step was to shuffle the segments and divide the segmented data into a training and testing set. This was done through the scikit-learn function train_test_split with the shuffle flag set to True and the test_size parameter set to 0.1.

To summarize the work so far, DataFrames were created to hold each member's walking and jumping data, all combined walking and jumping data, and all combined data, and NumPy arrays were created to hold the 5-second segments and their classification, the data and associated labels for training set, and the data and associated labels for the test set. 

## Preprocessing
The purpose of preprocessing the data is to identify anomalies and other qualities within the dataset that may interfere with the performance of a model. The group opted to create a function that automates this process for the desired use case with the foresight that the same process would need to run on multiple datasets (i.e. training set, test set, inputted data, etc.). 

The first step of the function is dealing with missing values. As the data is a continuous set of readings from the sensors, there were not expected to be any missing values in the data, and this was simply implemented to increase the robustness of the model. The function first replaces any '-' with NaNs, and then populates the NaNs using linear interpolation. This method was chosen as interpolation maintains the trend in the continuous data, and is overall more accurate than sample-and-holding.

The data was then normalized using scikit-learn's StandardScaler method. The function implements z-score normalization to transform the data to a mean of 0 and a standard deviation of 1. This is done using the formula $z = (x-\mu)/\sigma$, where $z$ is the outputted score, $x$ is the original value, $\mu$ is the mean, and $\sigma$ is the standard deviation. The following figure demonstrates the effect of the normalization on one of the segments. The range within the data has decreased, but the values remain proportional to each other. 

<div align="center"><img src="https://github.com/D-Joseph/MovementClassification/assets/67702022/3c14e63a-d98f-48ad-b658-844edbbe07fe" width="50%"></div>

The final preprocessing work that is done is through a moving average filter which will help reduce the noise within the data. Noise can degrade the quality of data by obscuring or destroying features within a signal. Noise generally occurs in two types, high-frequency and low-frequency. High-frequency noise can obscure underlying trends and make it difficult to detect patterns, while low-frequency noise can bias results and lead to inaccurate conclusions. 
Several potential sources of noise exist within this dataset, such as if a person's hand moves or if the phone rotates slightly, as this would populate the accelerometer reading with acceleration that is unrelated to the walking or jumping motion. Furthermore, vibrations from a notification could also lead to additional high-frequency noise within the sensor data. 

To remove noise from this dataset, a simple moving average (MA) filter was used. An MA filter is known as a 'low-pass filter,' meaning that it permits low frequencies within the data and omits high frequencies. The MA filter calculates the average of a fixed number of consecutive data points in the time series, where the number of data points used in the calculation is called the window size. The window is then moved forward one data point at a time, and the process is repeated for each new window until the end of the time series is reached. 

To determine the optimal window size for this project, the data after the MA filter was applied was plotted and visually inspected. A large window size would lead to significant smoothing at the cost of information loss. The group decided that a window size of 20 provided sufficient smoothing for the first iteration of the model. 
## Feature Extraction
The purpose of feature extraction is to extract key information that represents the data, without using the entire dataset. For this project, several characteristics of each segment were calculated and then fed into the model during both training and testing. The extracted features were minimum, maximum, mean, median, skewness, kurtosis, standard deviation, variance, and root mean square. As the extraction took place on each segment, this step was integrated within the preprocessing step, after the simple moving average filter took place.

## Classifier Training
Following feature extraction, a Logistic Regression (LR) model was used to classify the data. LR classifiers are generally used for binary classification problems where the goal is to predict one of two outcomes, such as walking or jumping.

The Logistic Regression model was created using the *LogisticRegression* class from scikit-learn. The only parameter that was used was the maximum number of iterations which was set to 10,000 to ensure that the model had enough time to converge and find an optimal solution [1]. The default value of *max_iter* is 100, which may not be sufficient for complex datasets such as the walking and jumping data used for this project. The trade-off of using such a high value is that it may increase the training time of the model. Although the method used in the lectures and lab was...

To evaluate the performance of the model, several metrics and plots were used. This includes accuracy, recall, F1 score, and the Area Under the Curve (AUC).

The first iteration's results are summarized in the below table:
| Accuracy | Recall | F1 Score | AUC   |
|----------|--------|----------|-------|
| 0.788    | 0.778  | 0.795    | 0.835 |

### Iterations
With an accuracy shy of 80%, the group was confident that changes could be made to improve it. The window size used for the MA filter was changed to 26, as this tended to yield the highest accuracy, F1 score, and recall. The group then opted to try different classifiers and settled on Random Forests with 10,000 trees. These changes then produced the following performance:
| Accuracy | Recall | F1 Score | AUC   |
|----------|--------|----------|-------|
| 0.941    | 0.911  | 0.988    | 0.943 |

## Model Deployment
The goal of this step was to create an intuitive, engaging user interface that would allow the user to directly interact with the model. The Graphical User Interface (GUI) was created using the Tkinter library instead of PyQT5 as it was noted to be more beginner-friendly and faster to implement. In short, the GUI first asks the user to select a CSV that contains the walking/jumping data, displays a plot of the data, and then asks the user to select where to save the labelled version of the input.

To prevent having to constantly retrain the classifier, the pickle library was used to save the model and allow for its use across the program. Additionally, as the prediction occurs across 5-second windows, a design choice was made for the input file to be truncated to the nearest multiple of 500 (this assumes the 100Hz collection frequency on Apple devices, and is similar to the operation done on the raw dataset). The alternative is to have unlabelled rows in the outputted CSV, however, the group deemed this undesirable.

To test the system to ensure that it works as intended, the testing files that were inputted were limited to only walking or only jumping. This was done such that the user could know the actual output for the given segments, and could verify if the model predicted correctly. If the file were a mixture of both walking and jumping, this would be a much harder task as it would not necessarily be clear what action the user performed during a given window. The limit to one action also is the motivation for the dominant prediction being displayed.
