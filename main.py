import hashlib

class Block:
    def __init__(self, node, trust, prev_hash):
        self.node = node
        self.trust = trust
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.node) + str(self.trust) + str(self.prev_hash)
        return hashlib.sha256(data.encode()).hexdigest()


import networkx as nx
import numpy as np
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

# 🔹 Step 1: Create 200 IoT nodes
# 🔹 Step 1: Create IoT Network
G = nx.Graph()
num_nodes = 100

node_ips = {}

for i in range(num_nodes):
    G.add_node(i)
    node_ips[i] = f"192.168.1.{i+1}"

# 🔹 Step 2: Create connections
for i in range(num_nodes):
    for j in range(i + 1, num_nodes):
        if random.random() < 0.05:
            G.add_edge(i, j)

# 🔹 Step 3: Malicious nodes
malicious_nodes = random.sample(range(num_nodes), int(0.2 * num_nodes))
centrality = nx.degree_centrality(G)
for node in G.nodes():
    G.nodes[node]['malicious'] = node in malicious_nodes

# 🔹 Step 4: Initialize storage
data = []
packet_logs = []
success_count = 0
drop_count = 0

node_success = {i: 0 for i in range(num_nodes)}
node_drop = {i: 0 for i in range(num_nodes)}

protocols = ["TCP", "UDP", "ICMP"]

# 🔹 Step 5: Simulation loop
for node in G.nodes():

    # -------- Feature generation FIRST --------
    attack_types = ["DoS", "Delay", "Normal"]
    if random.random() < 0.4:
        attack = random.choice(["DoS", "Delay"])
    else:
        attack = "Normal"

    if attack == "DoS":
        pdr = np.random.uniform(0.2, 0.5)
        drop = np.random.uniform(0.5, 0.9)
        delay = np.random.uniform(5, 10)

    elif attack == "Delay":
        pdr = np.random.uniform(0.6, 0.8)
        drop = np.random.uniform(0.2, 0.4)
        delay = np.random.uniform(8, 15)

    else:  # Normal
        pdr = np.random.uniform(0.8, 1.0)
        drop = np.random.uniform(0.0, 0.2)
        delay = np.random.uniform(1, 5)

    freq = np.random.uniform(5, 20)

    energy = 1 + (drop * 3) + (delay * 0.1)

    label = 0 if attack == "Normal" else 1
   

    # -------- Packet simulation AFTER features --------
    neighbors = list(G.neighbors(node))
    if neighbors:
        dest = random.choice(neighbors)

        src_ip = node_ips[node]
        dst_ip = node_ips[dest]
        protocol = random.choice(protocols)

        if random.random() < drop:
            status = "Dropped"
            drop_count += 1
            node_drop[node] += 1
        else:
            status = "Success"
            success_count += 1
            node_success[node] += 1

        packet_logs.append([src_ip, dst_ip, protocol, status])

    # -------- Store data --------
    data.append([pdr, drop, delay, freq, energy, label])

# 🔹 Step 6: Convert to DataFrame
df = pd.DataFrame(data, columns=[
    "PDR", "DropRate", "Delay", "Frequency", "Energy", "Label"
])

# 🔹 Step 7: Packet DataFrame
packet_df = pd.DataFrame(packet_logs, columns=[
    "Source", "Destination", "Protocol", "Status"
])
# 🔹 Node-wise reliability
node_reliability = []

for node in range(num_nodes):
    total = node_success[node] + node_drop[node]
    if total == 0:
        reliability = 1
    else:
        reliability = node_success[node] / total

    node_reliability.append(reliability)

df["NodeReliability"] = node_reliability

df["Centrality"] = [centrality[i] for i in range(num_nodes)]

# 🔹 Step 6: ML Model (Edge node logic)
X = df.drop("Label", axis=1)
y = df["Label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(n_estimators=50)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print("ML Accuracy:", accuracy)

# 🔹 Step 7: Trust calculation (baseline)
df["Trust"] = 0.7 * df["PDR"] - 0.3 * df["DropRate"]
neighbor_trusts = []

for node in G.nodes():
    neighbors = list(G.neighbors(node))
    if neighbors:
        avg_neighbor_trust = np.mean([df.loc[n, "Trust"] for n in neighbors])
    else:
        avg_neighbor_trust = df.loc[node, "Trust"]

    final_trust = 0.6 * df.loc[node, "Trust"] + 0.4 * avg_neighbor_trust
    neighbor_trusts.append(final_trust)

df["FinalTrust"] = neighbor_trusts
# 🔹 Packet-based trust (global)
packet_trust = success_count / (success_count + drop_count + 1e-5)

# 🔹 Hybrid Trust (NEW - BEST FEATURE)
df["HybridTrust"] = (
    0.4 * df["FinalTrust"] +
    0.25 * packet_trust +
    0.2 * df["NodeReliability"] +
    0.15 * df["Centrality"]
)

# 🔹 Blockchain initialization
blockchain = []
prev_hash = "0"

for node in range(num_nodes):
    block = Block(node, df.loc[node, "HybridTrust"], prev_hash)
    blockchain.append(block)
    prev_hash = block.hash
# 🔹 Neighbor visualization table data

import json

block_data = []

for b in blockchain:
    block_data.append({
        "node": b.node,
        "trust": float(b.trust),
        "prev_hash": b.prev_hash,
        "hash": b.hash
    })

with open("blockchain.json", "w") as f:
    json.dump(block_data, f)
neighbor_info = []

for node in G.nodes():
    neighbors = list(G.neighbors(node))

    if neighbors:
        avg_neighbor_trust = round(np.mean([df.loc[n, "Trust"] for n in neighbors]), 3)
    else:
        avg_neighbor_trust = df.loc[node, "Trust"]

    neighbor_info.append([
        node,
        str(neighbors[:3]),  # show only first 3 neighbors
        round(df.loc[node, "Trust"], 3),
        round(avg_neighbor_trust, 3),
        round(df.loc[node, "FinalTrust"], 3)
    ])

neighbor_df = pd.DataFrame(neighbor_info, columns=[
    "Node", "Neighbors", "Own Trust", "Neighbor Avg", "Final Trust"
])

print("\nSample Blockchain Entries:")
for b in blockchain[:5]:
    print(f"Node: {b.node}, Trust: {round(b.trust,3)}, Hash: {b.hash[:10]}")

# 🔹 Step 8: Plot Trust graph
# 🔹 Trust graph
plt.figure(figsize=(14, 8))
plt.plot(df["FinalTrust"], label="Neighbor Trust")
plt.plot(df["HybridTrust"], label="Hybrid Trust")
plt.legend()
plt.title("Trust Values of Nodes")
plt.xlabel("Node Index")
plt.ylabel("Trust")

# 🔹 Network graph
plt.figure(figsize=(14, 10))

pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
colors = ["red" if df.loc[n, "Label"] == 1 else "green" for n in G.nodes()]

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

fig, axs = plt.subplots(2, 3, figsize=(16, 10))

# 🔹 Trust vs Time
trust_over_time = []

for t in range(10):
    temp_pdr = df["PDR"] + np.random.normal(0, 0.05, len(df))
    temp_drop = df["DropRate"] + np.random.normal(0, 0.05, len(df))

    temp_pdr = temp_pdr.clip(0, 1)
    temp_drop = temp_drop.clip(0, 1)

    trust = 0.7 * temp_pdr - 0.3 * temp_drop
    trust += np.random.normal(0, 0.02, len(df))

    # 🔥 ADD randomness
   

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
attack_counts = df["Label"].value_counts()

axs[0, 2].bar(["Normal", "Malicious"], attack_counts)
axs[0, 2].set_title("Attack Distribution")
axs[1, 0].bar(["Baseline", "ML"], [baseline_computations, ml_computations], width=0.3)
axs[1, 0].set_title("Computations")

axs[1, 2].bar(["Success", "Dropped"], [success_count, drop_count])
axs[1, 2].set_title("Packet Stats")

# 🔹 Confusion Matrix
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(cm)
disp.plot(ax=axs[1, 1])
axs[1, 1].set_title("Confusion Matrix")

plt.tight_layout()

plt.figure(figsize=(14, 6))

# 🔹 LEFT: Neighbor Trust Table
plt.subplot(1, 2, 1)
plt.axis('off')

table1 = plt.table(
    cellText=neighbor_df.head(10).values,
    colLabels=neighbor_df.columns,
    loc='center'
)

table1.auto_set_font_size(False)
table1.set_fontsize(8)

plt.title("Neighbor Trust Influence")

# 🔹 RIGHT: Packet Logs
plt.subplot(1, 2, 2)
plt.axis('off')

table2 = plt.table(
    cellText=packet_df.head(10).values,
    colLabels=packet_df.columns,
    loc='center'
)

table2.auto_set_font_size(False)
table2.set_fontsize(8)

plt.title("Packet Logs")

plt.tight_layout()


plt.title("Packet Transmission Stats")
plt.ylabel("Count")
plt.show()