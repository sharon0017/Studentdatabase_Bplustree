# B+ Tree-Based Large-Scale Student Database Indexing System

## 📌 Project Overview
This project is a Data Structures and Data Algorithms (DSDA) case study implementing a custom B+ Tree Indexing Engine from scratch. It simulates a high-performance database layer capable of handling massive-scale academic records, supporting both logarithmic point lookups and highly efficient sequential range queries.

---

## 📖 Data Structure Justification
We chose a **B+ Tree** over other data structures because it is the only structure optimized for both massive-scale exact match queries and range queries.

* **Why not Hash Tables?** Hash tables offer $O(1)$ point lookups but completely fail at range queries (e.g., finding all students with a GPA between 3.5 and 4.0). A hash table would require an inefficient $O(N)$ full table scan.
* **Why not AVL or Red-Black Trees?** Binary search trees have a strict fan-out factor of 2, leading to deep trees. B+ Trees have a high fan-out (Order $M$), making the tree significantly shallower, which drastically minimizes node access times and traversal depth.
* **Why not standard B-Trees?** Standard B-trees store payload data inside internal nodes. B+ Trees restrict data strictly to leaf nodes, allowing internal nodes to hold more routing keys per block. This maximizes the fan-out factor and keeps the tree shallow.

---

## 🏗 Implementation Strategy
Our architectural choices prioritize modularity and low-level memory efficiency. 

* **Node Representation (Polymorphism):** We implemented a base `BPlusNode` class extended by `InternalNode` (holds only routing keys and child pointers) and `LeafNode` (holds actual `StudentRecord` objects).
* **Linked Leaf Architecture:** The most critical structural decision was adding `next` and `prev` pointers to the `LeafNode` class. This creates a doubly-linked list exclusively at the bottom tier of the tree.
* **Trade-off Justification:** Maintaining these sibling pointers adds slight memory overhead and complexity during node-splitting operations. However, it successfully reduces range query time from requiring multiple $O(\log N)$ tree traversals down to $O(K)$ horizontal pointer hops.

---

## ⚙️ Edge Case Handling & Fault Tolerance
The application includes a custom exception-handling layer (`student_record.py`) to ensure the live program does not crash during unexpected user inputs:
1. **`DuplicateKeyException`:** Prevents database corruption if an existing Student ID is inserted.
2. **`RecordNotFoundException`:** Gracefully alerts the user if a point search target does not exist, rather than throwing a null pointer error.
3. **`InvalidQueryRangeException`:** Blocks structurally invalid range queries (e.g., when the Start ID is greater than the End ID).
4. **Data Validation:** Enforces logical constraints before data touches the tree (e.g., GPA must be between 0.0 and 4.0).

---

## ⏱ Time Complexity Analysis
The system operates on an Order $M$ (maximum children per node).

| Operation | Time Complexity | Mathematical Justification |
| :--- | :--- | :--- |
| **Point Search** | $O(\log_M N)$ | At each level, the algorithm narrows the search space by a factor of $M$. Because data is only in leaves, every search drops exactly to the height of the tree. |
| **Range Query** | $O(\log_M N + K)$ | It takes $O(\log_M N)$ to traverse from the root to the first matching leaf. Retrieving the remaining $K$ elements requires $O(K)$ sequential steps horizontally via the linked list, entirely bypassing the tree structure above. |
| **Insertion** | $O(\log_M N)$ | Traversing to the correct leaf takes $O(\log_M N)$. If a node overflows, splitting takes $O(M)$ time, but splits are infrequent enough that the amortized complexity remains strictly logarithmic. |
| **Auxiliary Space**| $O(N)$ | The tree scales linearly with the number of inserted records. |

---

## 👥 Team Contributions & Architecture Roles
This project was built collaboratively, with code divided into modular components pushed via individual GitHub accounts.

* **[Your Name]**: Built the Data Schema & Validation Engine (`student_record.py`) and authored the DSDA theoretical analysis (`README.md`).
* **[Member 2 Name]**: Designed the Core Algorithm Architecture (`bplus_tree.py`) including the bottom-up node splitting logic.
* **[Member 3 Name]**: Engineered the polymorphic node hierarchy and linked-list structures (`bplus_node.py`).
* **[Member 4 Name]**: Developed the interactive Command Line Interface, telemetry tracking, and exception handling loop (`main.py`).