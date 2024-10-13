---
title: 【C++ STL】数值算法stl_numeric.h
author: zhugenmi
date: 2024-10-13
categories: [C++, STL]
tags: [c++]
---

```cpp
#include <numeric>
#include <vector>
#include <functional>
#include <iostream>
#include <cmath>
#include <iterator> //ostream_iterator
using namespace std;

int main()
{
    int ia[5] = {1, 2, 3, 4, 5};
    vector<int> iv(ia, ia + 5);

    // 求初值0与区间[iv.begin(),iv.end())之间元素的和
    cout << accumulate(iv.begin(), iv.end(), 0) << endl;
    // 0+1+2+3+4+5=15

    cout << accumulate(iv.begin(), iv.end(), 0, minus<int>()) << endl;
    // 0-1-2-3-4-5=-15

    cout << inner_product(iv.begin(), iv.end(), iv.begin(), 10) << endl;
    // 内积 10+1*1+2*2+3*3+4*4+5*5=65

    cout << inner_product(iv.begin(), iv.end(), iv.begin(), 10, minus<int>(), plus<int>()) << endl;
    // 10-(1+1)-(2+2)-(3+3)-(4+4)-(5+5)=-20

    // 以下迭代器将绑定到cout，作为输出用
    ostream_iterator<int> oite(cout, " ");

    partial_sum(iv.begin(), iv.end(), oite);
    // 1 3 6 10 15(第n个元素是前n个旧元素的和)
    cout << endl;

    partial_sum(iv.begin(), iv.end(), oite, minus<int>());
    // 1 -1 -4 -8 -13(第n个元素是前n个旧元素的运算总和)
    cout << endl;

    adjacent_difference(iv.begin(), iv.end(), oite);
    cout << endl;
    // 1 1 1 1 1(#1元素不变，#n元素等于#n旧元素 - #n-1旧元素)

    adjacent_difference(iv.begin(), iv.end(), oite, plus<int>());
    cout << endl;
    // 1 3 5 7 9(#1元素不变，#n元素等于op(#n旧元素, #n-1旧元素))

    cout << pow(10, 3) << endl;
    // cout<<pow(10,3,plus<int>())<<endl;

    int n = 3;
    iota(iv.begin(), iv.end(), n); // 在指定区间填入n,n+1,n+2...
    for (int i = 0; i < iv.size(); ++i)
    {
        cout << iv[i] << " "; // 3 4 5 6 7
    }
}

```
