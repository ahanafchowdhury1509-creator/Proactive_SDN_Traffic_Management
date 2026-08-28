from collections import deque
graph={
    1:[2,3],
    2:[1,4],
    3:[1,4],
    4:[2,3]
}

def bfs_path(graph,start,goal):
    queue=deque()
    queue.append(start)
    came_from={start:None}
    while queue:
        cur=queue.popleft()
        if cur==goal:
            break
        for neigh in graph[cur]:
            if neigh not in came_from:
                queue.append(neigh)
                came_from[neigh]=cur
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur)
        cur=came_from[cur]
    path.reverse()
    return path
    