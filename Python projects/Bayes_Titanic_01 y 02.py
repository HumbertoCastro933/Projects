import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report

data = pd.read_csv("titanic.csv")

# Seleccionar características 
data = data[["Survived", "Pclass", "Sex", "Age", "Fare"]]

# Preprocesamiento:

# Manejo de valores faltantes
data["Age"].fillna(data["Age"].mean(), inplace=True)

# Convertir variable categórica "Sex" a numérica
data["Sex"] = data["Sex"].map({"male": 0, "female": 1})

# Dividir datos en características (X) y etiqueta (y) 
X = data[["Pclass", "Sex", "Age", "Fare"]]
y = data["Survived"]

# Dividir conjunto en train y test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar modelo Bayesiano
modelo = GaussianNB()
modelo.fit(X_train, y_train)

# Predecir
y_pred = modelo.predict(X_test)

# Evaluar
print("Exactitud (accuracy):", accuracy_score(y_test, y_pred))
print("\nReporte de Clasificación:\n", classification_report(y_test, y_pred))

# Graficar dos características Edad y Tarifa 
plt.figure(figsize=(8,6))
plt.scatter(data["Age"][data["Survived"] == 1],
            data["Fare"][data["Survived"] == 1],
            color="green", label="Sobrevivió", alpha=0.6)
plt.scatter(data["Age"][data["Survived"] == 0],
            data["Fare"][data["Survived"] == 0],
            color="red", label="No sobrevivió", alpha=0.6)
plt.title("Relación entre Edad y Tarifa según Supervivencia")
plt.xlabel("Edad")
plt.ylabel("Tarifa (Fare)")
plt.legend()
plt.grid(True)
plt.show()
