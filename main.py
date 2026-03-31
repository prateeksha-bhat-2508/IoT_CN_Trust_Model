import networkx as nx
import numpy as np
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

# 🔹 Step 1: Create 200 IoT nodes
G = nx.Graph()
num_nodes = 100

for i in range(num_nodes):
    G.add_node(i)

# 🔹 Step 2: Random connections
for i in range(num_nodes):
    for j in range(i+1, num_nodes):
        if random.random() < 0.05:  # lower prob for large graph
            G.add_edge(i, j)

# 🔹 Step 3: Malicious nodes (20%)
malicious_nodes = random.sample(range(num_nodes), int(0.2 * num_nodes))

for node in G.nodes():
    G.nodes[node]['malicious'] = node in malicious_nodes

# 🔹 Step 4: Generate features
data = []

for node in G.nodes():
    if G.nodes[node]['malicious']:
        pdr = np.random.uniform(0.2, 0.6)
        drop = np.random.uniform(0.4, 0.8)
    else:
        pdr = np.random.uniform(0.7, 1.0)
        drop = np.random.uniform(0.0, 0.3)

    delay = np.random.uniform(1, 10)
    freq = np.random.uniform(5, 20)
    # base energy
    base_energy = np.random.uniform(1, 3)

    # increase energy based on behavior
    energy = base_energy + (drop * 3) + (delay * 0.1)

    label = 1 if G.nodes[node]['malicious'] else 0

    data.append([pdr, drop, delay, freq, energy, label])

# 🔹 Step 5: DataFrame
df = pd.DataFrame(data, columns=[
    "PDR", "DropRate", "Delay", "Frequency", "Energy", "Label"
])

# 🔹 Step 6: ML Model (Edge node logic)
X = df.drop("Label", axis=1)
y = df["Label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print("ML Accuracy:", accuracy)

# 🔹 Step 7: Trust calculation (baseline)
df["Trust"] = 0.7 * df["PDR"] - 0.3 * df["DropRate"]

# 🔹 Step 8: Plot Trust graph
# 🔹 Trust graph
plt.figure(figsize=(14, 8))
plt.plot(df["Trust"])
plt.title("Trust Values of Nodes")
plt.xlabel("Node Index")
plt.ylabel("Trust")

# 🔹 Network graph
plt.figure(figsize=(14, 10))

pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
colors = ["red" if G.nodes[n]['malicious'] else "green" for n in G.nodes()]

nx.draw(
    G, pos,
    node_color=colors,
    node_size=100,
    edge_color="gray",
    width=0.5,
    alpha=0.7,
    with_labels=True,
    font_size=7
)

plt.title("IoT Network Graph")

# ✅ SINGLE show at the end

fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# 🔹 Trust vs Time
trust_over_time = []
for t in range(10):
    df["PDR"] += np.random.normal(0, 0.02, len(df))
    df["DropRate"] += np.random.normal(0, 0.02, len(df))

    df["PDR"] = df["PDR"].clip(0, 1)
    df["DropRate"] = df["DropRate"].clip(0, 1)

    trust = 0.7 * df["PDR"] - 0.3 * df["DropRate"]
    trust_over_time.append(trust.mean())

axs[0, 0].plot(trust_over_time, marker='o')
axs[0, 0].set_title("Trust vs Time")

# 🔹 Energy
normal_energy = df[df["Label"] == 0]["Energy"].mean()
malicious_energy = df[df["Label"] == 1]["Energy"].mean()

axs[0, 1].bar(["Normal", "Malicious"], [normal_energy, malicious_energy], width=0.3)
axs[0, 1].set_title("Energy")

# 🔹 Computations
baseline_computations = len(df) * 10
ml_computations = len(df)

axs[1, 0].bar(["Baseline", "ML"], [baseline_computations, ml_computations], width=0.3)
axs[1, 0].set_title("Computations")

# 🔹 Confusion Matrix
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(cm)
disp.plot(ax=axs[1, 1])
axs[1, 1].set_title("Confusion Matrix")

plt.tight_layout()
plt.show()