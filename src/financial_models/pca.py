from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from src.utils import config
import matplotlib.pyplot as plt


df = pd.read_csv("data/stocks.csv",delimiter=",")
df.duplicated().sum()




scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df)

pca = PCA(n_components=2)
df_pca = pca.fit_transform(df_scaled)



cc = []
for i in range(1,21):
    kmeans = KMeans(n_clusters=i,init='k-means++',n_init=20,random_state=42).fit(df_pca)
    cc.append(kmeans.inertia_)


plt.plot(range(1,21),cc,marker='*')
plt.xlabel('Clusters')
plt.ylabel('Inertia')
plt.title('The Elbow Method')
plt.show()



kmeans = KMeans(n_clusters=16,init='k-means++',n_init=20,random_state=42).fit(df_pca)
labels = kmeans.fit_predict(df_pca)
df['Cluster'] = kmeans.labels_



plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            s=200,
            marker='X',
            color='black',
            edgecolors='w',
            label='Cluster Centroids')

plt.xlabel('Principal Component 1 (PC1)')
plt.ylabel('Principal Component 2 (PC2)')
plt.title('K-Means Clustering of Stock Data (PCA-Reduced)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
