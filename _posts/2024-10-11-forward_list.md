---
title: 【C++ STL】forward_list
author: zhugenmi
date: 2024-10-11 
categories: [C/C++, STL]
tags: [c++,forward_list]
---

## 说明

定义于头文件 `<forward_list>`

```cpp
template<
    class T,
    class Allocator = std::allocator<T>
> class forward_list;
```

`std::forward_list` 是支持从容器中的任何位置快速插入和移除元素的容器。不支持快速随机访问。它实现为单链表，且实质上与其在 C 中实现相比无任何开销。与 `std::list` 相比，此容器提高在不需要双向迭代时提供更有效地利用空间的存储。

在链表内或跨数个链表添加、移除和移动元素，不会非法化当前指代链表中其他元素的迭代器。然而，在从链表移除元素（通过 `erase_after` ）时，指代对应元素的迭代器或引用会被非法化。

## 方法

| 元素访问 |                               |
| -------- | ----------------------------- |
| front    | 访问第一个元素 (公开成员函数) |

| 迭代器                      |                                               |
| --------------------------- | --------------------------------------------- |
| before_begin  cbefore_begin | 返回指向第一个元素之前迭代器 (公开成员函数)   |
| begin  cbegin               | 返回指向容器第一个元素的迭代器 (公开成员函数) |
| end  cend                   | 返回指向容器尾端的迭代器 (公开成员函数)       |

| 容量     |                                       |
| -------- | ------------------------------------- |
| empty    | 检查容器是否为空 (公开成员函数)       |
| max_size | 返回可容纳的最大元素数 (公开成员函数) |

| 修改器        |                                           |
| ------------- | ----------------------------------------- |
| clear         | 清除内容 (公开成员函数)                   |
| insert_after  | 在某个元素后插入新元素 (公开成员函数)     |
| emplace_after | 在元素后原位构造元素 (公开成员函数)       |
| erase_after   | 擦除元素后的元素 (公开成员函数)           |
| push_front    | 插入元素到容器起始 (公开成员函数)         |
| emplace_front | 在容器头部就地构造元素 (公开成员函数)     |
| pop_front     | 移除首元素 (公开成员函数)                 |
| resize        | 改变容器中可存储元素的个数 (公开成员函数) |
| swap          | 交换内容 (公开成员函数)                   |

| 操作              |                                             |
| ----------------- | ------------------------------------------- |
| merge             | 合并二个已排序列表 (公开成员函数)           |
| splice_after      | 从另一 forward_list 移动元素 (公开成员函数) |
| remove  remove_if | 移除满足特定标准的元素 (公开成员函数)       |
| reverse           | 将该链表的所有元素的顺序反转 (公开成员函数) |
| unique            | 删除连续的重复元素 (公开成员函数)           |
| sort              | 对元素进行排序 (公开成员函数)               |

### splice_after()

从另一 `forward_list` 移动元素到 *this 。

不复制元素。 `pos` 为 `*this` 中的合法迭代器，或 `before_begin()` 迭代器。若 `get_allocator() != other.get_allocator()` 则行为未定义。没有迭代器或引用被非法化，指向被移动的元素的迭代器现在指代到 `*this` 中，而非 `other` 中。

```cpp
void splice_after( const_iterator pos, forward_list& other ); // 从 other 移动所有元素到 *this 。元素被插入到 pos 所指向的元素后。操作后 other 变为空。若 other 与 *this 指代同一对象则行为未定义。

void splice_after( const_iterator pos, forward_list& other,
const_iterator it );//从 other 移动后随 it 的迭代器所指向的元素到 *this 。元素被插入到 pos 所指向的元素后，若 pos==it 或若 pos==++it 则无效果。

void splice_after( const_iterator pos, forward_list& other,
const_iterator first, const_iterator last );//从 other 移动范围 (first, last) 中的元素到 *this 。元素被插入到 pos 所指向的元素后。不移动 first 所指向的元素。若 pos 是范围 (first,last) 中的元素则行为未定义。
```

注意第三种形式中开区间 (first, last) 的含义：不移动 l1 的首元素。

## 示例

```cpp
#include <forward_list>
#include <string>
#include <iostream>
#include <vector>

template <typename T>
std::ostream &operator<<(std::ostream &s, const std::forward_list<T> &v)
{
    s.put('[');
    char comma[3] = {'\0', ' ', '\0'};
    for (const auto &e : v)
    {
        s << comma << e;
        comma[0] = ',';
    }
    return s << ']';
}

int main()
{
    std::forward_list<std::string> words{"the", "frogurt", "is", "also", "cursed"};
    std::cout << "words: " << words << '\n';

    // insert_after (2)
    auto beginIt = words.begin();
    words.insert_after(beginIt, "strawberry");
    std::cout << "words: " << words << '\n';

    // insert_after (3)
    auto anotherIt = beginIt;
    ++anotherIt;
    anotherIt = words.insert_after(anotherIt, 2, "Strawberry");
    std::cout << "words: " << words << '\n';

    // insert_after (4)
    std::vector<std::string> V = {"apple", "banana", "cherry"};
    anotherIt = words.insert_after(anotherIt, V.begin(), V.end());
    std::cout << "words: " << words << '\n';

    // insert_after (5)
    words.insert_after(anotherIt, {"jackfruit", "kiwifruit", "lime", "mango"});
    std::cout << "words: " << words << '\n';

    std::forward_list<int> l1 = {1, 2, 3, 4, 5};
    std::forward_list<int> l2 = {10, 11, 12};

    l2.splice_after(l2.cbegin(), l1, l1.cbegin(), l1.cend());
    // not equivalent to l2.splice_after(l2.cbegin(), l1);

    std::cout << "l1: " << l1 << '\n'; // 1
    std::cout << "l2: " << l2 << '\n'; // 10, 2, 3, 4, 5, 11, 12
}
```

输出：

```she
words: [the, frogurt, is, also, cursed]
words: [the, strawberry, frogurt, is, also, cursed]
words: [the, strawberry, Strawberry, Strawberry, frogurt, is, also, cursed]
words: [the, strawberry, Strawberry, Strawberry, apple, banana, cherry, frogurt, is, also, cursed]
words: [the, strawberry, Strawberry, Strawberry, apple, banana, cherry, jackfruit, kiwifruit, lime, mango, frogurt, is, also, cursed]
l1: [1]
l2: [10, 2, 3, 4, 5, 11, 12]
```