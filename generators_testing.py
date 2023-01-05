def __order_by(l:list()):
    for i in l:
        i = i + 1
        yield i
    yield None


def traverse_linked_list():
    # this is a list just for testing purposes
    l = [1, 2, 3, 4]
    current_node = 0
    order = __order_by(l)
    while True:
        node = next(order, None)
        yield node
        current_node += 1


gen = traverse_linked_list()


while True:
    n = next(gen)
    if n is None:
        break
    print(n)




