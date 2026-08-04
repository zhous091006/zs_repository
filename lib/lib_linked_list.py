from typing import Iterator, Any


class LibLinkedListNode:
    def __init__(self, data=None):
        self.data = data
        self.prev: [LibLinkedListNode, None] = None
        self.next: [LibLinkedListNode, None] = None


class LibLinkedList:
    def __init__(self):
        self.head = LibLinkedListNode()
        self.head.prev = self.head
        self.head.next = self.head

    def items(self) -> Iterator[LibLinkedListNode]:
        node = self.head.next
        while node != self.head:
            yield node
            node = node.next

    def datas(self) -> Iterator[Any]:
        node = self.head.next
        while node != self.head:
            yield node.data
            node = node.next

    def clear(self):
        while not self.is_empty():
            self.remove_node(self.head.next)

    def size(self):
        n = 0
        node = self.head.next
        while node != self.head:
            n += 1
            node = node.next
        return n

    def is_head(self, node: LibLinkedListNode):
        return node == self.head

    def first(self) -> [LibLinkedListNode, None]:
        if not self.is_empty():
            return self.head.next
        return None

    def is_empty(self):
        return self.head == self.head.next

    def prepend_data(self, data):
        item = LibLinkedListNode(data)
        item.next = self.head.next
        item.prev = self.head
        self.head.next.prev = item
        self.head.next = item

    def append_data(self, data):
        item = LibLinkedListNode(data)
        item.next = self.head
        item.prev = self.head.prev
        self.head.prev.next = item
        self.head.prev = item

    def insert_node(self, node: LibLinkedListNode, front_node: LibLinkedListNode):
        if self.is_node_existed(front_node):
            if self.is_node_existed(node):
                self.remove_node(node)
            node.next = front_node.next
            node.prev = front_node
            front_node.next.prev = node
            front_node.next = node

    def insert_data(self, data, front_node: LibLinkedListNode):
        node = LibLinkedListNode(data)
        self.insert_node(node, front_node)

    def remove_data(self, data):
        i_node = self.head.next
        while i_node != self.head:
            if i_node.data == data:
                tmp_node = i_node.next
                self.remove_node(i_node)
                i_node = tmp_node
            else:
                i_node = i_node.next

    def remove_node(self, node: LibLinkedListNode) -> bool:
        if self.is_node_existed(node):
            node.data = None
            node.prev.next = node.next
            node.next.prev = node.prev
            return True
        return False

    def is_data_existed(self, data) -> bool:
        return self.get_node_by_data(data) is not None

    def is_node_existed(self, node: LibLinkedListNode) -> bool:
        tmp_node = self.head.next
        while True:
            if tmp_node == node:
                return True
            tmp_node = tmp_node.next
            if tmp_node == self.head:
                break
        return False

    def get_node_by_data(self, data) -> [LibLinkedListNode, None]:
        for node in self.items():
            if node.data == data:
                return node
        return None
