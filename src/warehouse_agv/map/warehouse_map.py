"""Warehouse graph."""


class WarehouseMap:

    def __init__(self):

        self.nodes = {}

        self.edges = []

    def add_node(self, node):

        self.nodes[node.id] = node

    def add_edge(self, edge):

        self.edges.append(edge)
