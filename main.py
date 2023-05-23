# -*- coding: utf-8 -*-


class TreeStore:
    def __init__(self, items):
        self.tree = {}

        def build(sequence, parent='root'):
            return [
                {i['id']: {'item': {**i}, 'children': build(sequence, i['id'])}}
                for i in sequence if i['parent'] == parent
            ]

        if items:
            self.tree, *_ = build(items)

    def _fetch(self, data, result=[]):
        if isinstance(data, dict):
            for key, value in data.items():
                result.append(value['item'])
                self._fetch(value['children'], result)

        elif isinstance(data, list):
            for value in data:
                self._fetch(value, result)

        return result

    def _find(self, data, id, name='item'):
        if id in data:
            return data[id][name]

        result = {}
        if isinstance(data, dict):
            for key, value in data.items():
                result = self._find(value['children'], id, name)

                if id in result:
                    return result

        elif isinstance(data, list):
            for value in data:
                result = self._find(value, id, name)

                if id in result:
                    return result[id][name]
                elif result:
                    return result

        return result

    def getAll(self):
        return self._fetch(self.tree)

    def getItem(self, id):
        return self._find(self.tree, id)

    def getChildren(self, id):
        def prepare(item):
            ((_, value),) = item.items()
            return value['item']

        return list(
            map(prepare, self._find(self.tree, id, name='children'))
        )

    def getAllParents(self, id):
        result = []

        item = self._find(self.tree, id)
        result.append(item)

        while item['parent'] != 'root':
            item = self._find(self.tree, item['parent'])
            result.append(item)

        return result


ITEMS = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None}
]


if __name__ == '__main__':
    tree = TreeStore(ITEMS)

    print(tree.getAll())

    print(tree.getItem(4))

    print(tree.getChildren(4))

    print(tree.getAllParents(4))

