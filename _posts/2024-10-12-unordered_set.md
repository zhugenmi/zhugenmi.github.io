---
title: 【C++ STL】unordered_set
author: zhugenmi
date: 2024-10-12
categories: [C/C++, STL]
tags: [c++,unordered_set]
---
## 说明

定义于头文件 `<unordered_set>`

```cpp
template<
    class Key,
    class Hash = std::hash<Key>,
    class KeyEqual = std::equal_to<Key>,
    class Allocator = std::allocator<Key>
> class unordered_set;
```

`unordered_set` 是含有 Key 类型唯一对象集合的关联容器。搜索、插入和移除拥有平均常数时间复杂度。

在内部，元素并不以任何特别顺序排序，而是组织进桶中。元素被放进哪个桶完全依赖其值的哈希。这允许对单独元素的快速访问，因为哈希一旦，就准确指代元素被放入的桶。

不可修改容器元素（即使通过非 `const `迭代器），因为修改可能更改元素的哈希，并破坏容器。

>unordered_multiset 是关联容器，含有可能非唯一 Key 类型对象的集合。搜索、插入和移除拥有平均常数时间复杂度。元素在内部并不以任何顺序排序，只是被组织到桶中。元素被放入哪个桶完全依赖其值的哈希。这允许快速访问单独的元素，因为一旦计算哈希，它就指代放置该元素的准确的桶。

## 方法

| 迭代器        |                                               |
| ------------- | --------------------------------------------- |
| begin  cbegin | 返回指向容器第一个元素的迭代器 (公开成员函数) |
| end  cend     | 返回指向容器尾端的迭代器 (公开成员函数)       |

| 容量     |                                       |
| -------- | ------------------------------------- |
| empty    | 检查容器是否为空 (公开成员函数)       |
| size     | 返回容纳的元素数 (公开成员函数)       |
| max_size | 返回可容纳的最大元素数 (公开成员函数) |

| 修改器          |                                          |
| --------------- | ---------------------------------------- |
| clear           | 清除内容 (公开成员函数)                  |
| insert          | 插入元素或结点 (C++17 起) (公开成员函数) |
| emplace         | 原位构造元素 (公开成员函数)              |
| emplace_hint    | 使用hint就地构造元素 (公开成员函数)      |
| erase           | 擦除元素 (公开成员函数)                  |
| swap            | 交换内容 (公开成员函数)                  |
| extract (C++17) | 从另一容器释出结点 (公开成员函数)        |
| merge (C++17)   | 从另一容器接合结点 (公开成员函数)        |

| 查找             |                                                 |
| ---------------- | ----------------------------------------------- |
| count            | 返回匹配特定键的元素数量 (公开成员函数)         |
| find             | 寻找带有特定键的元素 (公开成员函数)             |
| contains (C++20) | 检查容器是否含有带特定关键的元素 (公开成员函数) |
| equal_range      | 返回匹配特定键的元素范围 (公开成员函数)         |

| 桶接口                              |                                                   |
| ----------------------------------- | ------------------------------------------------- |
| begin(size_type)  cbegin(size_type) | 返回一个迭代器，指向指定的桶的开始 (公开成员函数) |
| end(size_type)  cend(size_type)     | 返回一个迭代器，指向指定的桶的末尾 (公开成员函数) |
| bucket_count                        | 返回桶数 (公开成员函数)                           |
| max_bucket_count                    | 返回桶的最大数量 (公开成员函数)                   |
| bucket_size                         | 返回在特定的桶中的元素数量 (公开成员函数)         |
| bucket                              | 返回带有特定键的桶 (公开成员函数)                 |

| 哈希策略        |                                                              |
| --------------- | ------------------------------------------------------------ |
| load_factor     | 返回每个桶的平均元素数量 (公开成员函数)                      |
| max_load_factor | 管理每个桶的平均元素数量的最大值 (公开成员函数)              |
| rehash          | 为至少为指定数量的桶预留存储空间。  这会重新生成哈希表。 (公开成员函数) |
| reserve         | 为至少为指定数量的元素预留存储空间。  这会重新生成哈希表。 (公开成员函数) |

| 观察器        |                                             |
| ------------- | ------------------------------------------- |
| hash_function | 返回用于对关键哈希的函数 (公开成员函数)     |
| key_eq        | 返回用于比较键的相等性的函数 (公开成员函数) |



## 示例

```cpp
#include<iostream>
#include<unordered_set>

using namespace std;

struct CustomHash{
    size_t operator()(const string& key) const{
        return hash<string>()(key);
    }
};

int main(){
    // 创建一个 unordered_set
    unordered_set<string, CustomHash> mySet;

    // 插入元素
    mySet.insert("apple");
    mySet.insert("banana");
    mySet.insert("orange");
    mySet.insert("banana"); // 重复插入，unordered_set 会自动忽略

    // 输出元素
    cout << "当前元素: ";
    for (const auto& elem : mySet) {
        cout << elem << " ";
    }
    cout << endl;

    // 查找元素
    string key = "banana";
    if (mySet.find(key) != mySet.end()) {
        cout << "找到元素: " << key << endl;
    } else {
        cout << "未找到元素: " << key << endl;
    }

    // 使用 count 方法
    cout << "元素 'apple' 的数量: " << mySet.count("apple") << endl;

    // 获取桶信息
    cout << "桶的数量: " << mySet.bucket_count() << endl;
    cout << "最大桶的数量: " << mySet.max_bucket_count() << endl;

     // 获取特定桶的大小
    cout << "桶 0 中的元素数量: " << mySet.bucket_size(0) << endl; //1

    // 清空 unordered_set
    mySet.clear();
    cout << "清空后元素数量: " << mySet.size() << endl; //0

    // 重新插入元素
    mySet.insert("grape");
    mySet.insert("kiwi");

     // 使用 reserve 方法预留空间
    mySet.reserve(10);
    cout << "预留空间后桶的数量: " << mySet.bucket_count() << endl; //11

    // 输出当前元素
    cout << "当前元素: ";
    for (const auto& elem : mySet) {
        cout << elem << " ";
    }
    cout << endl;

    return 0;
}
```

