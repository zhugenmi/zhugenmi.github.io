---
title: 【C++ STL】priority_queue
author: zhugenmi
date: 2024-10-11 
categories: [C++, STL]
tags: [c++,priority_queue]
---

## 说明

priority_queue（优先队列）本质是一个堆，需包含头文件`#include<queue>`

```cpp
template<    
	class T,    
	class Container = std::vector<T>,    
	class Compare = std::less<typename Container::value_type> 
> class priority_queue;
```

priority_queue 是容器适配器，它提供常数时间的（默认）最大元素查找，对数代价的插入与释出。

可用用户提供的 Compare 更改顺序，例如，用 `std::greater<T>` 将导致最小元素作为 `top()` 出现。

用 priority_queue 工作类似管理某些随机访问容器中的堆，优势是不可能突然把堆非法化。

## 关于priority_queue中元素的比较

　　模板申明带3个参数：`priority_queue<Type, Container, Functional>`，其中Type 为数据类型，Container为保存数据的容器，Functional 为元素比较方式。

　　Container必须是用数组实现的容器，比如`vector`，`deque`等等，但不能用 list。STL里面默认用的是`vector`。比较方式默认用`operator<`，所以如果把后面2个参数缺省的话，优先队列就是大顶堆（降序），队头元素最大。特别注意pair的比较函数。

```cpp
template<class T>
priority_queue<T, vector<T>, less<T>> max_heap; //大顶堆
priority_queue<T, vector<T>, greater<T>> min_heap; //小顶堆
```

# 方法

| 元素访问        |                                           |
| --------------- | ----------------------------------------- |
| top             | 访问栈顶元素 (公开成员函数)               |
| empty           | 检查底层的容器是否为空 (公开成员函数)     |
| size            | 返回容纳的元素数 (公开成员函数)           |
| push            | 插入元素，并对底层容器排序 (公开成员函数) |
| emplace (C++11) | 原位构造元素并排序底层容器 (公开成员函数) |
| pop             | 删除第一个元素 (公开成员函数)             |
| swap            | 交换内容 (公开成员函数)                   |



# 示例

```cpp
#include <functional>
#include <queue>
#include <vector>
#include <iostream>
 
template<typename T> void print_queue(T& q) {
    while(!q.empty()) {
        std::cout << q.top() << " ";
        q.pop();
    }
    std::cout << '\n';
}
 
int main() {
    std::priority_queue<int> q; //默认大顶堆
 
    for(int n : {1,8,5,6,3,4,0,9,7,2})
        q.push(n);
 
    print_queue(q); //9 8 7 6 5 4 3 2 1 0 
 
    std::priority_queue<int, std::vector<int>, std::greater<int> > q2; //小顶堆
 
    for(int n : {1,8,5,6,3,4,0,9,7,2})
        q2.push(n);
 
    print_queue(q2); //0 1 2 3 4 5 6 7 8 9 
 
    // 用 lambda 比较元素。
    auto cmp = [](int left, int right) { return (left ^ 1) < (right ^ 1);};
    std::priority_queue<int, std::vector<int>, decltype(cmp)> q3(cmp);
 
    for(int n : {1,8,5,6,3,4,0,9,7,2})
        q3.push(n);
 
    print_queue(q3);//8 9 6 7 4 5 2 3 0 1

}
```

