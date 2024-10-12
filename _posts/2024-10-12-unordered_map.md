---
title: 【C++ STL】unordered_map
author: zhugenmi
date: 2024-10-12
categories: [C++, STL]
tags: [c++,unordered_map]
---
## 说明

定义于头文件 `<unordered_map>`

```cpp
template<
    class Key,
    class T,
    class Hash = std::hash<Key>,
    class KeyEqual = std::equal_to<Key>,
    class Allocator = std::allocator< std::pair<const Key, T> >
> class unordered_map;
```

`unordered_map` 是关联容器，含有带唯一键的键-值 pair 。搜索、插入和元素移除拥有平均常数时间复杂度。

元素在内部不以任何特定顺序排序，而是组织进桶中。元素放进哪个桶完全依赖于其键的哈希。这允许对单独元素的快速访问，因为一旦计算哈希，则它准确指代元素所放进的桶。

>unordered_multimap 是无序关联容器，支持等价的关键（一个 unordered_multimap 可含有每个关键值的多个副本）和将关键与另一类型的值关联。 unordered_multimap 类支持向前迭代器。搜索、插入和移除拥有平均常数时间复杂度。元素在内部不以任何特定顺序排序，而是组织到桶中。元素被放进哪个桶完全依赖于其关键的哈希。这允许到单独元素的快速访问，因为哈希一旦计算，则它指代元素被放进的准确的桶。



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

| 修改器                   |                                                           |
| ------------------------ | --------------------------------------------------------- |
| clear                    | 清除内容 (公开成员函数)                                   |
| insert                   | 插入元素或结点 (C++17 起) (公开成员函数)                  |
| insert_or_assign (C++17) | 插入元素，或若关键已存在则赋值给当前元素 (公开成员函数)   |
| emplace                  | 原位构造元素 (公开成员函数)                               |
| emplace_hint             | 使用hint就地构造元素 (公开成员函数)                       |
| try_emplace (C++17)      | 若键不存在则原位插入，若键存在则不做任何事 (公开成员函数) |
| erase                    | 擦除元素 (公开成员函数)                                   |
| swap                     | 交换内容 (公开成员函数)                                   |
| extract (C++17)          | 从另一容器释出结点 (公开成员函数)                         |
| merge (C++17)            | 从另一容器接合结点 (公开成员函数)                         |

| 查找             |                                                 |
| ---------------- | ----------------------------------------------- |
| at               | 访问指定的元素，同时进行越界检查 (公开成员函数) |
| [operator]       | 访问或插入指定的元素 (公开成员函数)             |
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
#include <iostream>
#include <unordered_map>
#include <string>

using namespace std;

int main() {
    // Create an unordered_map
    unordered_map<string, int> myMap;

    // Insert elements
    myMap.insert({"apple", 1});
    myMap.insert({"banana", 2});
    myMap.insert({"orange", 3});

    // Insert or assign (C++17)
    myMap.insert_or_assign("banana", 5); // Updates the value for "banana"
    
    // Emplace elements
    myMap.emplace("grape", 4);

    // Try emplace (C++17)
    myMap.try_emplace("apple", 10); // Does not change the value for "apple"

    // Output elements
    cout << "Current elements in the unordered_map:" << endl;
    for (const auto& pair : myMap) {
        cout << pair.first << ": " << pair.second << endl;
    }

    // Find an element
    string key = "banana";
    if (myMap.find(key) != myMap.end()) {
        cout << "Found element: " << key << " with value: " << myMap[key] << endl;
    } else {
        cout << "Element not found: " << key << endl;
    }

    // Count occurrences of a key
    cout << "Count of 'orange': " << myMap.count("orange") << endl;

    // Accessing an element with at() method
    try {
        cout << "Value of 'grape': " << myMap.at("grape") << endl; //4
    } catch (const out_of_range& e) {
        cout << e.what() << endl;
    }

    // Bucket information
    cout << "Bucket count: " << myMap.bucket_count() << endl; //13
    cout << "Max bucket count: " << myMap.max_bucket_count() << endl; //164703072086692425
    cout << "Bucket size for bucket 0: " << myMap.bucket_size(0) << endl; //2

    // Clear the unordered_map
    myMap.clear();
    cout << "Size after clearing: " << myMap.size() << endl; //0

    // Reinsert elements
    myMap["kiwi"] = 6;
    myMap["mango"] = 7;

    // Reserve space
    myMap.reserve(10);
    cout << "Bucket count after reserving space: " << myMap.bucket_count() << endl; //11

    // Output current elements
    cout << "Current elements after reinsertion:" << endl;
    for (const auto& pair : myMap) {
        cout << pair.first << ": " << pair.second << endl;
    }

    return 0;
}
```

