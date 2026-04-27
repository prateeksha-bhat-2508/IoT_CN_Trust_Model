<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>IoT Trust Management System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
            background-color: #f8f9fa;
            color: #333;
        }
        h1, h2 {
            color: #0d6efd;
        }
        code, pre {
            background: #eee;
            padding: 5px;
            border-radius: 5px;
        }
        pre {
            padding: 10px;
            overflow-x: auto;
        }
        ul {
            margin-left: 20px;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>

<div class="container">

<h1>🚀 IoT Trust Management System using ML & Blockchain</h1>

<h2>📌 Overview</h2>
<p>
This project simulates an IoT network and evaluates the trustworthiness of nodes using machine learning, 
network metrics, and a lightweight blockchain mechanism. It detects malicious behavior and ensures secure, 
tamper-resistant storage of trust values.
</p>

<h2>🧠 Key Features</h2>
<ul>
    <li>🔗 IoT Network Simulation using graph-based topology</li>
    <li>🤖 Machine Learning Detection for identifying malicious nodes</li>
    <li>📊 Hybrid Trust Model combining:
        <ul>
            <li>Node behavior (PDR, Drop Rate, Delay)</li>
            <li>Neighbor influence</li>
            <li>Packet reliability</li>
            <li>Graph centrality</li>
        </ul>
    </li>
    <li>🔐 Blockchain Integration for secure and immutable trust storage</li>
    <li>🌳 Merkle Tree Visualization for data integrity verification</li>
</ul>

<h2>⚙️ Tech Stack</h2>
<ul>
    <li>Python</li>
    <li>NetworkX</li>
    <li>NumPy & Pandas</li>
    <li>Scikit-learn</li>
    <li>Matplotlib</li>
    <li>Streamlit</li>
</ul>

<h2>🏗️ System Architecture</h2>
<pre>
IoT Network Simulation (NetworkX)
            ↓
Feature Extraction (PDR, Delay, Drop Rate, etc.)
            ↓
Machine Learning Model (Random Forest)
            ↓
Hybrid Trust Calculation
            ↓
Blockchain Storage (Hash + Previous Hash)
            ↓
Visualization (Graphs + Merkle Tree + UI)
</pre>

<h2>🔗 Blockchain Implementation</h2>
<ul>
    <li>Each node’s trust value is stored as a <b>block</b></li>
    <li>Each block contains:
        <ul>
            <li>Node ID</li>
            <li>Trust Value</li>
            <li>Previous Hash</li>
            <li>Current Hash</li>
            <li>(Optional) Nonce & Merkle Root</li>
        </ul>
    </li>
    <li>Blocks are linked using hash pointers → ensures <b>immutability</b></li>
    <li>Merkle Tree used for <b>hierarchical hash verification</b></li>
</ul>

<h2>📊 Outputs</h2>
<ul>
    <li>Trust value graphs (Node-wise & Time-based)</li>
    <li>IoT network visualization</li>
    <li>Packet transmission statistics</li>
    <li>Confusion matrix (ML performance)</li>
    <li>Blockchain visualization</li>
    <li>Merkle tree structure</li>
</ul>

<h2>▶️ How to Run</h2>

<h3>1. Run Backend (Generate Data)</h3>
<pre>python main.py</pre>

<h3>2. Run Frontend (Visualization)</h3>
<pre>streamlit run app.py</pre>

<h2>📁 Project Structure</h2>
<pre>
IoT_Trust_Model/
│
├── main.py              # Core simulation + ML + blockchain
├── app.py               # Streamlit visualization
├── blockchain.json      # Generated blockchain data
└── README.md
</pre>

<h2>💡 Future Improvements</h2>
<ul>
    <li>Real-time integration with network simulators (NS3 / Packet Tracer)</li>
    <li>Advanced blockchain (Proof-of-Work / Smart Contracts)</li>
    <li>Deep learning-based anomaly detection</li>
    <li>Live IoT data integration</li>
</ul>

<h2>💬 Summary</h2>
<p>
This project combines <b>network simulation, machine learning, and blockchain</b> to build a secure and intelligent 
trust evaluation system for IoT environments.
</p>

</div>

</body>
</html>