
# 🛡️ Ethereum ERC-20 Transaction Tracing & AML Detection

This repository showcases the **MSc Dissertation Project** titled:  
**"Implementation and Validation of the Ethereum JSON-RPC API for ERC-20 Token Transaction Retrieval and Money Laundering Detection"**  
by **Juilee Gund**, University of Birmingham, 2023–2024.

## 📘 Abstract

This project implements Ethereum's JSON-RPC API to retrieve and analyze ERC-20 token transaction data from the blockchain. It demonstrates a cost-effective and scalable method to detect suspicious money laundering activity in decentralized finance (DeFi) ecosystems — **without using expensive services like QuickNode**.

The solution includes:

- Direct interaction with an Ethereum node (E-Node) using WebSocket and JSON-RPC.
- Extraction, decoding, and validation of token transfer logs.
- Network visualization of token flows to identify suspicious behavior.
- Comparative evaluation with a QuickNode instance.

---

## 📁 Project Structure

```
📂 MSc Cybersecurity Dissertation/
├── 📄 MSc_Dissertation_JUILEE.pdf
├── 📄 presentation.pptx
├── 📂Scripts/
    ├── 📄 script_1_data_extraction.py
    ├── 📄 script_2_data_validation.py
    ├── 📄 script_3_data_export.py
    ├── 📄 script_4_visualization.py
└── 📄 README.md
```

### 🔧 Python Scripts

- `script_1_data_extraction.py`  
  Connects to the Ethereum E-Node and extracts ERC-20 token transaction data using JSON-RPC methods.

- `script_2_data_validation.py`  
  Validates extracted data against QuickNode outputs for accuracy.

- `script_3_data_export.py`  
  Exports transaction data to Excel format for further analysis and visualization.

- `script_4_visualization.py`  
  Uses Plotly & Dash Cytoscape to create network graphs of token transfers.

---

## 🧪 Tools & Technologies

- **Ethereum JSON-RPC API**
- **Python 3.8+**
- **Web3.py**
- **Plotly & Dash Cytoscape**
- **Tailscale VPN** (for secure node access)
- **QuickNode** (used for validation only)

---

## 🎯 Key Features

- Retrieves ERC-20 token transactions (e.g., USDC, USDT, BADGER).
- Visualizes wallet-to-wallet token flows.
- Flags suspicious behaviors (e.g., smurfing, layering).
- Validates custom node data against commercial nodes.
- Demonstrates viable, open-access alternatives to premium blockchain analytics tools.

---

## 📸 Demo

> 📎 A PowerPoint presentation (`presentation.pptx`) is included to walk through the implementation, methodology, results, and conclusions.  
> For visual examples, see figures in the dissertation PDF (`MSc_Dissertation_JUILEE.pdf`).

---

## 📚 Dissertation

For complete methodology, background research, evaluation, and references, please refer to the full dissertation document provided in the repository.

---

## 📬 Contact

**Author:** Juilee Gund  
**Supervisor:** Dr. Pascal Berrang  
**University:** University of Birmingham – School of Computer Science  
**Year:** 2023–24

---

## 📝 License

This repository is for academic and educational use. Please cite or credit appropriately when referencing this work.
