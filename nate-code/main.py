import heapq # aka python's binary tree

def bound(node, n, capacity, items):
    # invalid node check
    if node['weight'] >= capacity:
        return 0
    
    profit_bound = node['value']
    j = node['level'] + 1
    total_weight = node['weight']

    # Keep adding to the profit bound until we reach capacity (find a hopeful upper bound)
    while j < n and total_weight + items[j]['weight'] <= capacity:
        total_weight += items[j]['weight']
        profit_bound += items[j]['value']
        j += 1
    if j < n:
        profit_bound += (capacity - total_weight) * items[j]['ratio']
    return profit_bound

def knapsack(capacity, items, n):
    Q = []
    # root node where no items have been considered
    cur = {'level': -1, 'value': 0, 'weight': 0, 'bound': 0}
    child = {'level': -1, 'value': 0, 'weight': 0, 'bound': 0}
    cur['bound'] = bound(cur, n, capacity, items)
    maxProfit = 0
    heapq.heappush(Q, (-cur['bound'], cur))
    while Q:
        _, cur = heapq.heappop(Q)
        # Essentially skipping over nodes that don't have as promising of a bound
        if cur['bound'] > maxProfit:
            # INCLUDING ITEM
            child['level'] = cur['level'] + 1
            child['weight'] = cur['weight'] + items[child['level']]['weight']
            child['value'] = cur['value'] + items[child['level']]['value']

            # check for new max profit value
            if child['weight'] <= capacity and child['value'] > maxProfit:
                maxProfit = child['value']

            # calculate and check if bound is good
            child['bound'] = bound(child, n, capacity, items)
            if child['bound'] > maxProfit:
                heapq.heappush(Q, (-child['bound'], child.copy()))

            # EXCLUDING ITEM
            child['weight'] = cur['weight']
            child['value'] = cur['value']

            # calculate and check if bound is good
            child['bound'] = bound(child, n, capacity, items)
            if child['bound'] > maxProfit:
                heapq.heappush(Q, (-child['bound'], child.copy()))
    return maxProfit

def main():
    with open('test.txt', 'r') as file:
        capacity, n = map(int, file.readline().split())
        items = []

        for line in file:
            value, weight = map(int, line.split())
            items.append({'value': value, 'weight': weight, 'ratio': value / weight})

        # Sort items by value/weight ratio (so bounding prioritizes best items)
        items.sort(key=lambda x: x['ratio'], reverse=True)
        maxProfit = knapsack(capacity, items, n)
        print(f"Maximum profit: {maxProfit}") # Expecting: 2493893

if __name__ == "__main__":
    main()