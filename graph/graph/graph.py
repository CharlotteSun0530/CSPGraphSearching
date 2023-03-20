# 首先读取文件并构建图
graph = {}
colors = 0
with open('gc_78317103208800.txt') as f:
    for line in f:
        if line.startswith('#'):
            continue
        if line.startswith('colors'):
            colors = int(line.split('=')[1].strip())
        else:
            v1, v2 = map(int, line.strip().split(','))
            if v1 not in graph:
                graph[v1] = set()
            if v2 not in graph:
                graph[v2] = set()
            graph[v1].add(v2)
            graph[v2].add(v1)

# 初始化待处理约束队列
queue = [(v1, v2) for v1 in graph for v2 in graph[v1]]

# 构建初始状态，所有节点都未被染色
init_state = {}

# 定义一个函数来检查当前的状态是否合法
def is_valid(state):
    for node in state:
        for neighbor in graph[node]:
            if neighbor in state and state[neighbor] == state[node]:
                return False
    return True

# 定义一个函数来使用AC3算法进行约束传播
def ac3(queue, domains):
    while queue:
        v1, v2 = queue.pop(0)
        if remove_inconsistent_values(v1, v2, domains):
            if not domains[v1]:
                return False
            for neighbor in graph[v1]:
                if neighbor != v2:
                    queue.append((neighbor, v1))
    return True

# 定义一个函数来移除不一致的取值
def remove_inconsistent_values(v1, v2, domains):
    removed = False
    for value in domains[v1]:
        if not any(value != d for d in domains[v2]):
            domains[v1].remove(value)
            removed = True
    return removed

# 定义一个函数来搜索解空间
def search(state, domains, heuristic):
    if len(state) == len(graph):
        return state
    node = min(set(graph.keys()) - set(state), key=lambda n: heuristic(n, state, domains))
    for color in domains[node]:
        new_state = state.copy()
        new_domains = domains.copy()
        new_state[node] = color
        new_domains[node] = [color]
        if is_valid(new_state) and ac3(queue[:], new_domains):
            result = search(new_state, new_domains, heuristic)
            if result is not None:
                return result
    return None

# 初始化颜色的取值范围
domains = {node: list(range(colors)) for node in graph}

# 启发式函数1：最小剩余值
def min_remaining_values(node, state, domains):
    return len(domains[node])

# 启发式函数2：最小约束值
def min_constraint_values(node, state, domains):
    count = 0
    for neighbor in graph[node]:
        if neighbor in state and state[neighbor] in domains[node]:
            count += 1
    return count

# 启发式函数3：组合启发式
def combined_heuristic(node, state, domains):
    return min_remaining_values(node, state, domains) * min_constraint_values(node, state, domains)

# 选择启发式函数
heuristic = combined_heuristic

# 开始搜索解空间
result = search(init_state, domains, heuristic)

if result is not None:
    print("Solution found:")
    for node, color in result.items():
        print(f"Node {node} has color {color}")
else :
    print("No solution found")

