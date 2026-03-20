import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# ==========================================
# 1. CARGA Y PREPARACIÓN DE DATOS
# ==========================================

def cargar_datos():
    """
    Intenta cargar 'datos_galletas.csv'. Si no existe, crea un DataFrame
    simulado basado en los datos del PDF 'Galletas_TV.pdf' para que el código funcione.
    """
    try:
        # Intenta cargar tu archivo si ya lo convertiste
        df = pd.read_csv('datos_galletas.csv')
        print("Archivo CSV cargado exitosamente.")
        return df
    except FileNotFoundError:
        print("No se encontró 'datos_galletas.csv'. Creando datos de prueba basados en el PDF...")
        # Datos simulados extraídos manualmente de las tablas del PDF para el ejemplo
        data = {
            'Tamaño': [40, 50, 120, 40, 50, 152, 42, 45, 48, 52],
            'Sabor':  [0, 2, 0, 1, 2, 0, 1, 0, 2, 2], # 0, 1, 2 son códigos
            'Textura':[1, 0, 2, 1, 1, 1, 1, 0, 0, 1],
            'Peso':   [10, 15, 9, 11, 6, 11, 9.9, 9, 15, 4],
            'Color':  ['0,0,0', '240,180,192', '255,225,120', '232,215,145', '222,184,135', 
                       '10,10,10', '50,50,50', '46,35,2', '100,100,100', '200,200,200'],
            'Calorias': [53, 56, 46, 50, 40, 55.4, 38.1, 54.8, 60.2, 30],
            'Azucar':   [3.5, 12, 3.3, 3.2, 0.96, 3.38, 2.9, 5.4, 3.2, 2],
            'Etiqueta': [0, 1, 2, 3, 4, 3, 2, 1, 0, 4] # La clase a predecir
        }
        # Multiplicamos los datos para tener suficientes para entrenar
        df = pd.DataFrame(data)
        df = pd.concat([df]*10, ignore_index=True) 
        # Añadimos un poco de ruido aleatorio para que no sean idénticos
        noise = np.random.normal(0, 0.5, [len(df), 3]) 
        df[['Tamaño', 'Peso', 'Calorias']] += noise
        return df

# Cargar el DataFrame
df = cargar_datos()

# ==========================================
# 2. PREPROCESAMIENTO
# ==========================================

print("\n--- Preprocesamiento ---")

# a) Limpieza de la columna Color (Separar RGB)
# El PDF muestra colores como "240.180.192" o "240,180,192"
def split_color(color_str):
    try:
        # Reemplazar puntos por comas si es necesario y separar
        parts = str(color_str).replace('.', ',').split(',')
        if len(parts) == 3:
            return int(parts[0]), int(parts[1]), int(parts[2])
    except:
        pass
    return 0, 0, 0 # Valor por defecto si falla

# Aplicar la separación
rgb = df['Color'].apply(lambda x: split_color(x))
df['R'] = [x[0] for x in rgb]
df['G'] = [x[1] for x in rgb]
df['B'] = [x[2] for x in rgb]

# Eliminar columna original de Color y otras columnas no numéricas si sobran
df = df.drop(columns=['Color'])

# b) Separar características (X) y etiqueta (y)
X = df.drop(columns=['Etiqueta'])
y = df['Etiqueta']

# c) Dividir en conjunto de Entrenamiento (70%) y Prueba (30%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# d) Escalado de datos (Crucial para KNN y SVM)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Datos procesados. Entrenamiento: {X_train.shape[0]} muestras. Prueba: {X_test.shape[0]} muestras.")

# ==========================================
# 3. ENTRENAMIENTO Y EVALUACIÓN DE ALGORITMOS
# ==========================================

resultados = {}

# --- Algoritmo 1: K-Vecinos más Cercanos (KNN) ---
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
y_pred_knn = knn.predict(X_test_scaled)
acc_knn = accuracy_score(y_test, y_pred_knn)
resultados['KNN'] = acc_knn

# --- Algoritmo 2: Teorema de Bayes (Gaussian Naive Bayes) ---
gnb = GaussianNB()
gnb.fit(X_train_scaled, y_train) # Bayes a veces no necesita escalado, pero no le hace daño
y_pred_gnb = gnb.predict(X_test_scaled)
acc_gnb = accuracy_score(y_test, y_pred_gnb)
resultados['Naive Bayes'] = acc_gnb

# --- Algoritmo 3: Máquinas de Soporte Vectorial (SVM) ---
svm = SVC(kernel='linear', random_state=42) # Probamos kernel lineal (puedes cambiar a 'rbf')
svm.fit(X_train_scaled, y_train)
y_pred_svm = svm.predict(X_test_scaled)
acc_svm = accuracy_score(y_test, y_pred_svm)
resultados['SVM'] = acc_svm

# ==========================================
# 4. REPORTAR RESULTADOS
# ==========================================

print("\nResultados de Exactitud (Accuracy):")
for nombre, acc in resultados.items():
    print(f"{nombre}: {acc*100:.2f}%")

# Imprimir reporte detallado del mejor modelo (ejemplo)
mejor_modelo = max(resultados, key=resultados.get)
print(f"\nEl modelo con mayor aceptación fue: {mejor_modelo}")

if mejor_modelo == 'KNN':
    print("\nReporte detallado para KNN:")
    print(classification_report(y_test, y_pred_knn))
elif mejor_modelo == 'SVM':
    print("\nReporte detallado para SVM:")
    print(classification_report(y_test, y_pred_svm))
else:
    print("\nReporte detallado para Naive Bayes:")
    print(classification_report(y_test, y_pred_gnb))

# ==========================================
# 5. GRÁFICAS
# ==========================================

# Gráfica de barras comparativa
plt.figure(figsize=(10, 6))
barras = plt.bar(resultados.keys(), [v*100 for v in resultados.values()], color=['blue', 'green', 'orange'])
plt.xlabel('Algoritmos')
plt.ylabel('Porcentaje de Aciertos (%)')
plt.title('Comparación de Algoritmos de Clasificación de Galletas')
plt.ylim(0, 100)

# Añadir el valor encima de cada barra
for bar in barras:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.1f}%', ha='center', va='bottom')

plt.show()