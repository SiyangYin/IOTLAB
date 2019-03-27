from sklearn import linear_model, svm
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split, cross_val_score
import csv

CSVFILE = "input.csv"


class MLModule:
    def loadData(self, csvFile):
        data = []
        with open(csvFile, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                dic = {'gap': row[0], 'switch': row[1], 'arrive_gap': row[2]}
                data.append(dic)
        data = data[1:]
        return data

    def regression(self, data, target):
        model = None
        ##########################################
        # 1. Set model to linear regression model
        ##########################################
        # Hint: use linear_model
        # regr = linear_model.LinearRegression()

        ##########################################
        # 2. Split train and test datasets 70/30
        ##########################################
        # Hint: use train_test_split.


        ##########################################
        # 3. Fit model to training data
        ##########################################

        ##########################################
        # 4. Predict on test data
        ##########################################

        ##########################################
        # 5. Evaluate with MAE and MSE
        ##########################################
        MAE = 0
        MSE = 0

        print("Mean absolute error: " + str(MAE))
        print("Mean squared error: " + str(MSE))
        return model

    def classification(self, data, target):
        model = None
        ##########################################
        # 1. Set model to svm classifier
        ##########################################

        ##########################################
        # 2. Fit model to training data
        ##########################################

        ##########################################
        # 3. Cross Validation
        ##########################################
        # Hint: Use cross_val_score
        CVS = 0

        print("Cross validation score: " + str(CVS))
        return model

def predict(x_real):
    model = MLModule()
    data = model.loadData(CSVFILE)

    data_x = [[int(row['gap'])] for row in data]
    # data_x = [row['gap'] for row in data]
    data_y = [int(row['arrive_gap']) for row in data]
    data_y_classify = [int(row['switch']) for row in data]

    # Linear Regression
    reg = linear_model.LinearRegression()
    reg.fit(data_x, data_y)
    print(reg.coef_)
    print(reg.intercept_)

    # SVM
    clf = svm.SVC(gamma='scale')
    clf.fit(data_x, data_y_classify)
    print(clf.predict(x_real))
        #print(clf.predict([[i] for i in range(0, 250)]))


if __name__ == "__main__":
#     model = MLModule()
#     data = model.loadData(CSVFILE)
# 
#     data_x = [[int(row['gap'])] for row in data]
#     # data_x = [row['gap'] for row in data]
#     data_y = [int(row['arrive_gap']) for row in data]
#     data_y_classify = [int(row['switch']) for row in data]
# 
#     # Linear Regression
#     reg = linear_model.LinearRegression()
#     reg.fit(data_x, data_y)
#     print(reg.coef_)
#     print(reg.intercept_)
# 
#     # SVM
#     clf = svm.SVC(gamma='scale')
#     clf.fit(data_x, data_y_classify)
    #print(clf.predict([[i] for i in range(0, 250)]))

