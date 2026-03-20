import numpy as np
from sklearn import svm
from sklearn.datasets import make_blobs 
import matplotlib.pyplot as plt

# 1. Crear los datos 
X, y = make_blobs(n_samples=40, centers=2, random_state=6) 

# Graficar los datos originales
plt.scatter(X[:, 0], X[:, 1], c=y, s=30, cmap=plt.cm.Paired)
plt.title("Datos originales")
plt.show()

# 2. Crear el modelo LINEAL
maquina = svm.SVC(kernel='linear', C=1000)
maquina.fit(X, y)

# Graficar puntos para el modelo lineal
plt.scatter(X[:, 0], X[:, 1], c=y, s=30, cmap=plt.cm.Paired)
ax = plt.gca()
xlim = ax.get_xlim() 
ylim = ax.get_ylim()

# Crear la malla (grid) para evaluar el modelo
xx = np.linspace(xlim[0], xlim[1], 30)
yy = np.linspace(ylim[0], ylim[1], 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T 

# Obtener la función de decisión
Z = maquina.decision_function(xy).reshape(XX.shape) 

# Dibujar la frontera y los márgenes
ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5,
           linestyles=['--', '-', '--'])

# Dibujar los Vectores de Soporte 
ax.scatter(maquina.support_vectors_[:, 0],
           maquina.support_vectors_[:, 1], s=100,
           linewidth=1, facecolors='none', edgecolors='k')

plt.title("SVM Lineal: Vectores de soporte, frontera y margen")
plt.show()


# 3. Prueba con KERNEL NO LINEAL 
maquinanolineal = svm.SVC(kernel='rbf', gamma=0.7, C=1)
maquinanolineal.fit(X, y)

# Graficar
plt.scatter(X[:, 0], X[:, 1], c=y, s=30, cmap=plt.cm.Paired)
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

xx = np.linspace(xlim[0], xlim[1], 30)
yy = np.linspace(ylim[0], ylim[1], 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T

Z = maquinanolineal.decision_function(xy).reshape(XX.shape)

# Dibujar contornos no lineales
ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1],
           alpha=0.5, linestyles=['--', '-', '--']) 

# Dibujar vectores de soporte
ax.scatter(maquinanolineal.support_vectors_[:, 0], 
           maquinanolineal.support_vectors_[:, 1], s=100,
           linewidth=1, facecolors='none', edgecolors='k')

plt.title("SVM Kernel No Lineal (RBF)")
plt.show()
