import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import json
import hashlib

# Load blockchain
with open("blockchain.json", "r") as f:
    blockchain = json.load(f)

st.subheader("Blockchain (20 Test Nodes)")

G_chain = nx.DiGraph()

# 🔹 Take only 20 nodes
test_blocks = blockchain[:20]

# Add nodes
for i, block in enumerate(test_blocks):
    label = f"N:{block['node']}\nH:{block['hash'][:6]}"
    G_chain.add_node(i, label=label)

# Add edges
for i in range(len(test_blocks)-1):
    G_chain.add_edge(i, i+1)

# 🔹 LINEAR LAYOUT (no mess)
pos = {i: (i, 0) for i in range(len(test_blocks))}

labels = nx.get_node_attributes(G_chain, 'label')

plt.figure(figsize=(18, 3))
nx.draw(G_chain, pos,
        labels=labels,
        with_labels=True,
        node_color="lightblue",
        node_size=2500,
        font_size=8,
        arrows=True)

st.pyplot(plt)
st.subheader("📦 Block Explorer (Detailed View)")

# Scrollable container
with st.container(height=400):

    for i, block in enumerate(blockchain):
        st.markdown(f"""
        ### 🔷 Block {i}

        - **Node ID:** {block['node']}
        - **Trust Value:** {round(block['trust'], 4)}
        - **Previous Hash:** `{block['prev_hash']}`
        - **Current Hash:** `{block['hash']}`
        - **Nonce:** {block.get('nonce', 'N/A')}
        - **Merkle Root:** {block.get('merkle_root', 'N/A')}

        ---
        """)
# Merkle Tree
# ------------------------
st.subheader("Merkle Tree (20 Nodes)")

hashes = [b["hash"] for b in blockchain[:20]]

def hash_pair(a, b):
    return hashlib.sha256((a + b).encode()).hexdigest()

levels = [hashes]

# Build tree
while len(levels[-1]) > 1:
    current = levels[-1]
    next_level = []

    for i in range(0, len(current), 2):
        if i+1 < len(current):
            combined = hash_pair(current[i], current[i+1])
        else:
            combined = current[i]
        next_level.append(combined)

    levels.append(next_level)

# --------------------------
# GRAPH BUILD
# --------------------------
G = nx.DiGraph()
node_id = 0
node_map = {}

# Add nodes
for level_idx, level in enumerate(levels):
    for i, h in enumerate(level):
        node_map[(level_idx, i)] = node_id
        G.add_node(node_id, label=h[:6], level=level_idx, pos=i)
        node_id += 1

# Add edges
for level_idx in range(len(levels)-1):
    for i in range(len(levels[level_idx])):
        parent_index = i // 2
        G.add_edge(
            node_map[(level_idx, i)],
            node_map[(level_idx+1, parent_index)]
        )

# --------------------------
# CLEAN TREE LAYOUT
# --------------------------
pos = {}

max_width = len(levels[0])

for level_idx, level in enumerate(levels):
    width = len(level)
    spacing = max_width / width

    for i in range(width):
        node = node_map[(level_idx, i)]
        x = i * spacing
        y = -level_idx
        pos[node] = (x, y)

labels = nx.get_node_attributes(G, 'label')

plt.figure(figsize=(12, 8))
nx.draw(G, pos,
        labels=labels,
        with_labels=True,
        node_color="lightgreen",
        node_size=2000,
        font_size=8,
        arrows=False)

st.pyplot(plt)