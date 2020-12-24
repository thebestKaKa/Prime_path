# -*- coding: utf-8 -*-
import copy
import time


def loadGraph(fileName):
    filePath = "D:/Study/学习材料/软件测试/prime_path/test_cases" + "/" + fileName
    with open(filePath, 'r') as fr:
        line_count = 0
        for line in fr:
            if line_count == 0:
                line_count += 1
                continue
            line = line[1: -2]
            if line != '-1':
                graph[line_count - 1] = [int(j) for j in line.split(',')]
            else:
                graph[line_count - 1] = []
            line_count += 1


def check(x, path):
    temp_path = copy.deepcopy(path)
    if len(temp_path) > 0:
        temp_path.pop(0)  # 把刚开始放进去的key弹出来 简单路径可以和第一个一样
    while len(temp_path) > 0:
        if temp_path.pop() == x:
            return True
    return False


def getSimplePath():
    for key in graph.keys():
        path = [key]
        dfs(key, copy.deepcopy(path))
        path.pop()


def dfs(key, path):
    value = graph[key]
    for t in value:
        if not check(t, path):
            path.append(t)
            simple_path.append(copy.deepcopy(path))
            if path[0] != t:  # 未形成环则继续添加 否则结束
                dfs(t, copy.deepcopy(path))
            path.pop()


def getPrimePath():
    global prime_path
    prime_path = copy.deepcopy(simple_path)
    count1 = 0
    while count1 < len(prime_path):
        count2 = count1 + 1
        flag = False
        while count2 < len(prime_path):
            if isSub(prime_path[count1], prime_path[count2]):
                del (prime_path[count1])
                flag = True
                break
            elif isSub(prime_path[count2], prime_path[count1]):
                del (prime_path[count2])
                continue
            count2 += 1
        if not flag:
            count1 += 1


# 判断path1是否是path2的子路径
def isSub(path1, path2):
    len1, len2 = len(path1), len(path2)
    count = 0
    if len1 > len2:
        return False
    while count + len1 <= len2:
        if path2[count: count + len1] == path1:
            return True
        else:
            count += 1
    return False


def pathCompress():
    count = 0
    while count < len(simple_path):
        flag = True
        if simple_path[count][0] == simple_path[count][-1]:
            count += 1
            continue
        for key in graph.keys():
            if simple_path[count][0] in graph[key] and key not in simple_path[count][:-1]:
                del simple_path[count]
                flag = False
                break
        if not flag:
            continue
        if simple_path[count][0] == simple_path[count][-1]:
            count += 1
            continue
        for item in graph[simple_path[count][-1]]:
            if item not in simple_path[count][1:]:
                del simple_path[count]
                count -= 1
                break
        count += 1


def resultToFiles(fileName):
    filePath = "D:/Study/学习材料/软件测试/prime_path/myresult" + "/" + fileName
    with open(filePath, 'w') as fr:
        fr.write("graph = {\n")
        for g in graph.items():
            fr.write('\t' + str(g)[1:-1] + '\n')
        fr.write("}\n")
        fr.write("the number of primePath:%d" % (len(prime_path)) + '\n')
        count = 0
        for path in prime_path:
            count += 1
            fr.write("path" + str(count) + ': ' + str(path) + '\n')


start = time.time()
for i in range(16):
    graph = dict()
    simple_path = []
    prime_path = []
    graph.clear()
    loadGraph('case' + str(i) + '.txt')
    getSimplePath()
    pathCompress()
    # getPrimePath()
    prime_path = simple_path
    prime_path = sorted(prime_path, key=lambda a: (len(a), a))
    resultToFiles('result_' + str(i) + '.txt')
    print("case" + str(i) + "一共有 %d 条主要路径。" % (len(prime_path)))
end = time.time()
print("一共运行了 %s 秒" % (end - start))
