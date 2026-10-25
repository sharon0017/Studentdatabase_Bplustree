"""
File 2: bplus_node.py
Description: Node class definitions supporting internal indexing and leaf data storage.
"""

from typing import List, Optional
from student_record import StudentRecord

class BPlusNode:
    """Base class for B+ Tree nodes."""
    def __init__(self, is_leaf: bool = False):
        self.is_leaf: bool = is_leaf
        self.keys: List[int] = []


class InternalNode(BPlusNode):
    """
    Internal Node: Contains routing keys and pointers to child nodes.
    Does NOT store actual record payloads.
    """
    def __init__(self):
        super().__init__(is_leaf=False)
        self.children: List[BPlusNode] = []


class LeafNode(BPlusNode):
    """
    Leaf Node: Contains keys, StudentRecord payloads, and sibling pointers.
    Forms a doubly linked list at the bottom tier of the tree.
    """
    def __init__(self):
        super().__init__(is_leaf=True)
        self.records: List[StudentRecord] = []
        self.next: Optional['LeafNode'] = None
        self.prev: Optional['LeafNode'] = None