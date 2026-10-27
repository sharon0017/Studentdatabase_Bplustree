"""
File 3: bplus_tree.py
Description: B+ Tree indexing engine core implementing search, insert, split, and range algorithms.
"""

import math
from typing import List, Optional, Tuple
from student_record import (
    StudentRecord, DuplicateKeyException, 
    RecordNotFoundException, InvalidQueryRangeException
)
from bplus_node import BPlusNode, InternalNode, LeafNode


class BPlusTreeEngine:
    """Production-grade B+ Tree Engine designed for low-level Data Structure evaluation."""
    def __init__(self, order: int = 4):
        if order < 3:
            raise ValueError("B+ Tree Order (M) must be >= 3.")
        self.order: int = order
        self.max_keys: int = order - 1
        self.min_keys: int = math.ceil(order / 2) - 1
        self.root: Optional[BPlusNode] = None

        # Telemetry metrics
        self.node_access_count: int = 0
        self.key_comparison_count: int = 0

    def insert(self, record: StudentRecord) -> None:
        """Inserts a record; triggers bottom-up node splitting on overflow."""
        # Pre-check for duplicate key to ensure primary key integrity
        if self._key_exists(record.student_id):
            raise DuplicateKeyException(f"Insertion Error: Student ID {record.student_id} already exists.")

        if self.root is None:
            new_leaf = LeafNode()
            new_leaf.keys.append(record.student_id)
            new_leaf.records.append(record)
            self.root = new_leaf
            return

        # Split Root if full before descending
        if len(self.root.keys) == self.max_keys:
            new_root = InternalNode()
            new_root.children.append(self.root)
            self._split_child(new_root, 0, self.root)
            self.root = new_root

        self._insert_non_full(self.root, record)

    def _key_exists(self, student_id: int) -> bool:
        try:
            self.search(student_id)
            return True
        except RecordNotFoundException:
            return False

    def _split_child(self, parent: InternalNode, child_idx: int, child: BPlusNode) -> None:
        mid = len(child.keys) // 2
        promoted_key = child.keys[mid]

        if child.is_leaf:
            left_leaf: LeafNode = child
            right_leaf = LeafNode()

            right_leaf.keys = left_leaf.keys[mid:]
            right_leaf.records = left_leaf.records[mid:]

            left_leaf.keys = left_leaf.keys[:mid]
            left_leaf.records = left_leaf.records[:mid]

            # Maintain horizontal doubly linked list
            right_leaf.next = left_leaf.next
            if left_leaf.next:
                left_leaf.next.prev = right_leaf
            left_leaf.next = right_leaf
            right_leaf.prev = left_leaf

            parent.keys.insert(child_idx, promoted_key)
            parent.children.insert(child_idx + 1, right_leaf)
        else:
            left_internal: InternalNode = child
            right_internal = InternalNode()

            right_internal.keys = left_internal.keys[mid + 1:]
            right_internal.children = left_internal.children[mid + 1:]

            left_internal.keys = left_internal.keys[:mid]
            left_internal.children = left_internal.children[:mid + 1]

            parent.keys.insert(child_idx, promoted_key)
            parent.children.insert(child_idx + 1, right_internal)

    def _insert_non_full(self, node: BPlusNode, record: StudentRecord) -> None:
        if node.is_leaf:
            leaf: LeafNode = node
            idx = 0
            while idx < len(leaf.keys) and record.student_id > leaf.keys[idx]:
                idx += 1
            leaf.keys.insert(idx, record.student_id)
            leaf.records.insert(idx, record)
        else:
            internal: InternalNode = node
            idx = len(internal.keys) - 1
            while idx >= 0 and record.student_id < internal.keys[idx]:
                idx -= 1
            idx += 1

            child = internal.children[idx]
            if len(child.keys) == self.max_keys:
                self._split_child(internal, idx, child)
                if record.student_id > internal.keys[idx]:
                    idx += 1
            self._insert_non_full(internal.children[idx], record)

    def search(self, student_id: int) -> StudentRecord:
        """Point Lookup: O(log N) direct tree navigation."""
        self.node_access_count = 0
        self.key_comparison_count = 0

        if not self.root:
            raise RecordNotFoundException("Database is completely empty.")

        curr = self.root
        while not curr.is_leaf:
            self.node_access_count += 1
            internal: InternalNode = curr
            idx = 0
            while idx < len(internal.keys) and student_id >= internal.keys[idx]:
                self.key_comparison_count += 1
                idx += 1
            curr = internal.children[idx]

        self.node_access_count += 1
        leaf: LeafNode = curr
        for i, key in enumerate(leaf.keys):
            self.key_comparison_count += 1
            if key == student_id:
                return leaf.records[i]

        raise RecordNotFoundException(f"Record with Student ID {student_id} was not found.")

    def range_query(self, start_id: int, end_id: int) -> List[StudentRecord]:
        """Range Scan: O(log N + K) horizontal linked leaf scan."""
        if start_id > end_id:
            raise InvalidQueryRangeException(f"Invalid range bounds: start_id ({start_id}) cannot be greater than end_id ({end_id}).")

        self.node_access_count = 0
        self.key_comparison_count = 0
        results: List[StudentRecord] = []

        if not self.root:
            return results

        # Step 1: Traverse to starting leaf node
        curr = self.root
        while not curr.is_leaf:
            self.node_access_count += 1
            internal: InternalNode = curr
            idx = 0
            while idx < len(internal.keys) and start_id >= internal.keys[idx]:
                self.key_comparison_count += 1
                idx += 1
            curr = internal.children[idx]

        # Step 2: Linear scan across connected leaf node pointers
        leaf: Optional[LeafNode] = curr
        while leaf is not None:
            self.node_access_count += 1
            for i, key in enumerate(leaf.keys):
                self.key_comparison_count += 1
                if start_id <= key <= end_id:
                    results.append(leaf.records[i])
                elif key > end_id:
                    return results
            leaf = leaf.next

        return results

    def display_tree(self, node: Optional[BPlusNode] = None, level: int = 0) -> None:
        """Visualizes tree hierarchy in terminal for presentation screenshots."""
        if node is None:
            node = self.root
            print("\n=======================================================")
            print("               B+ TREE STRUCTURE VISUALIZER            ")
            print("=======================================================")
            if node is None:
                print("Tree is currently empty.")
                print("=======================================================\n")
                return

        indent = "    " * level
        if node.is_leaf:
            leaf: LeafNode = node
            print(f"{indent}[Leaf Level {level}] Keys: {leaf.keys}")
        else:
            internal: InternalNode = node
            print(f"{indent}[Internal Level {level}] Keys: {internal.keys}")
            for child in internal.children:
                self.display_tree(child, level + 1)

        if level == 0:
            print("=======================================================\n")