import seaborn as sns
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

titanic = sns.load_dataset('titanic')

features = ['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked']
X = titanic[features]
y = titanic['survived']

X['age'].fillna(X['age'].mean(), inplace=True)
X['embarked'].fillna(X['embarked'].mode()[0], inplace=True)
X['sex'] = LabelEncoder().fit_transform(X['sex'])
X['embarked'] = LabelEncoder().fit_transform(X['embarked'])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

knn_classifier = KNeighborsClassifier(n_neighbors=5)
knn_classifier.fit(X_train, y_train)

y_pred = knn_classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Precisión KNN Titanic: {accuracy*100:.2f}%')
print("\nReporte de clasificación:\n", classification_report(y_test, y_pred))
