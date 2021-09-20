from typing import Any, Dict, Set, List


class Node(object):
    def __init__(self, index: int, item: Any, prev_node=None, next_node=None):
        self.index = index
        self.item = item
        self.prev_node = prev_node
        self.next_node = next_node

    def __str__(self):
        return f'Node({self.index}: {self.item})'

    def __repr__(self):
        return f'Node({self.index}: {self.item})'


class LinkedMap(object):
    """
    有序Map
    """

    def __init__(self):
        self._head = None
        self._tail = None
        self._cur = None
        self._node_dict = {}

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, head: Node):
        self._head = head

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self, tail: Node):
        self._tail = tail

    def is_empty(self):
        return len(self._node_dict) == 0

    def sorted_indexes(self, reverse=False) -> List:
        indexes = list(self._node_dict.keys())
        indexes.sort(reverse=reverse)
        return indexes

    def __update_dict(self, node, index):
        self._node_dict[index] = node

    def put(self, index: int, item: Any):
        if index in self._node_dict:
            self._node_dict[index].item = item
            return
        node = Node(index, item)
        p = None
        n = None
        smaller_indexes = [i for i in self._node_dict.keys() if i < index]
        lager_indexes = [i for i in self._node_dict.keys() if i > index]
        if len(smaller_indexes) > 0:
            p = self._node_dict[max(smaller_indexes)]
        if len(lager_indexes) > 0:
            n = self._node_dict[min(lager_indexes)]
        self._node_dict[index] = node
        if p is None:
            self.head = node
        else:
            p.next_node = node
            node.prev_node = p
        if n is None:
            self.tail = node
        else:
            n.prev_node = node
            node.next_node = n

    def remove(self, item: Any):
        for index, node in self._node_dict.items():
            if node.item == item:
                self.remove_by_index(index)
                return
        if self.is_empty():
            return

    def remove_by_index(self, index: int):
        if index in self._node_dict:
            node = self._node_dict[index]
            p = node.prev_node
            n = node.next_node
            if p is not None:
                p.next_node = n
            else:
                self.head = n
            if n is not None:
                n.prev_node = p
            else:
                self.tail = p
            del self._node_dict[index]

    def clear(self):
        self._node_dict.clear()
        self.head = None
        self.tail = None

    def items(self):
        cur = self.head
        while cur:
            yield cur.index, cur
            cur = cur.next_node

    def node(self, index) -> Node:
        return self._node_dict.get(index, None)

    def __iter__(self):
        self.cur = self.head
        return self

    def __next__(self):
        if self.cur:
            n = self.cur
            self.cur = self.cur.next_node
            return n
        else:
            raise StopIteration

    def __getitem__(self, index: int):
        node = self.node(index)
        return node.item if node else None

    def __setitem__(self, index: int, value: Any):
        self.put(index, value)

    def __len__(self):
        return len(self._node_dict)

    def __contains__(self, index: int):
        return index in self._node_dict

    def __str__(self):
        return f'linked_map(head: {self.head}'

    def __repr__(self):
        return f'linked_map(head: {self.head}'


class EnhancedMap(object):
    """
    二维Map，每行是一个有序集合，每列是集合
    """
    def __init__(self):
        # 存放每一行数据
        # row(index) -> LinkedMap
        self._linked_maps = {}
        # 存放每一列数据
        # col(frame_index) -> {}
        self._hash_maps = {}

    def __check_row(self, row: int):
        if row not in self._linked_maps:
            self._linked_maps[row] = LinkedMap()

    def __check_col(self, col: int):
        if col not in self._hash_maps:
            self._hash_maps[col] = {}

    def add_col(self, col: int, data: Dict[int, Any]):
        for row, item in data.items():
            self.__check_row(row)
            self._linked_maps[row][col] = item
        self._hash_maps[col] = data

    def set_data(self, row: int, col: int, data: Any):
        self.__check_row(row)
        self.__check_col(col)
        self._linked_maps[row][col] = data
        self._hash_maps[col][row] = data

    def remove_data(self, row: int, col: int):
        if col in self._hash_maps:
            if row in self._hash_maps[col]:
                del self._hash_maps[col][row]
        if row in self._linked_maps:
            self._linked_maps[row].remove_by_index(col)

    def col(self, col: int) -> Dict[int, Any]:
        return self._hash_maps.get(col, None)

    def row(self, row: int) -> LinkedMap:
        return self._linked_maps.get(row, None)

    def get_data(self, row: int, col: int):
        if col in self._hash_maps:
            return self._hash_maps[col].get(row, None)

    def col_keys(self) -> Set[int]:
        return set(self._hash_maps.keys())

    def row_keys(self) -> Set[int]:
        return set(self._linked_maps.keys())

    def col_items(self):
        cols = list(self.col_keys())
        cols.sort()
        for c in cols:
            yield c, self._hash_maps[c]

    def row_items(self):
        rows = list(self.row_keys())
        rows.sort()
        for r in rows:
            yield r, self._linked_maps[r]

    def clear(self):
        self._linked_maps.clear()
        self._hash_maps.clear()


if __name__ == '__main__':
    m1 = {1: 'hello', 3: 'yes'}
    m2 = {2: 'no2', 3: 'yes2'}
    m3 = {1: 'hello3', 3: 'yes3'}
    em = EnhancedMap()
    em.add_col(1, m1)
    em.add_col(2, m2)
    em.add_col(3, m3)
    em.set_data(1, 1, 'abc')
    print(em.col_keys())
    for i, t in em.row_items():
        print(i, t)
    for j, d in t.items():
        print(j, d)
