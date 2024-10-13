---
title: 【C++ STL】仿函数（function object, 函数对象）
author: zhugenmi
date: 2024-10-13
categories: [C++, STL]
tags: [c++]
---

函数对象：一种具有函数特质的对象。

STL仿函数的分类，若以操作数(operand)的个数划分，可分为一元和二元仿函数，若以功能划分，可分为算术运算(Arithmetic)、关系运算(Rational)、逻辑运算(Logical)三大类。任何应用程序欲使用STL内建的仿函数，都必须含入头文件`<functional>`，SGI则将它们实际定义于`<stl_function.h>`。

## 算术类(Arithmetic)仿函数

STL内建的“算术类仿函数”，支持加法、减法、乘法、除法、模数(余数，modulus)和否定(negation)运算，除了“否定”运算为一元运算，其它都是二元运算。

- 加法：`plus<T>`
- 减法：`minus<T>`
- 乘法：`multiplies<T>`
- 除法：`divides<T>`

例如：

```c++
template <class T>
struct plus : public binary_function<T, T, T>
{
    T operator()(const T &x, const T &y) const { return x + y; }
};

template <class T>
struct divides : public binary_function<T, T, T>
{
    T operator()(const T &x, const T &y) const { return x / y; }
};

template <class T>
struct negata : public unary_function<T, T>
{
    T operator()(cosnt T &x) const { return -x; }
};
```

> `unary_function`用来呈现一元函数的参数型别和回返值型别。`binary_function`用来呈现二元函数的第一参数型别、第二参数型别，以及回返值型别。

## 关系运算符(Relational)仿函数

STL内建的“关系运算类仿函数”支持了等于、不等于、大于、大于等于、小于、小于等于六种运算，每一个都是二元运算。

- 等于(equality): `equal_to<T>`
- 不等于(inequality): `not_equal_to<T>`
- 大于(greater than): `greater<T>`
- 大于或等于(greater than or equal): `greater_equal<T>`
- 小于(less than): `less<T>`
- 小于等于(less than or equal): `less_equal<T>`

例如：

```c++
template <class T>
struct equal_to : public binary_function<T, T, bool>
{
    bool operator()(const T &x, const T &y) const { return x == y; }
};

template <class T>
struct greater : public binary_function<T, T, bool>
{
    bool operator()(const T &x, const T &y) const { return x > y; }
};

template <class T>
struct less_equal : public binary_function<T, T, bool>
{
    bool  operator()(const T &x, const T &y) const { return x <= y; }
};
```

## 逻辑运算类(Logical)仿函数

STL内建的“逻辑运算类仿函数”支持了逻辑运算中的And、Or、Not三种运算，其中And和Or为二元运算，Not为一元运算。

- 逻辑运算And: `logical_and<T>`
- 逻辑运算Or: `logical_or<T>`
- 逻辑运算Not: `logical_not<T>`

例如：

```c++
template <class T>
struct logical_and : public binary_function<T, T, bool>
{
    bool operator()(const T &x, const T &y) const { return x && y; }
};

template <class T>
struct logical_or : public binary_function<T, T, bool>
{
    bool operator()(const T &x, const T &y) const { return x || y; }
};

template <class T>
struct logical_not : public unary_function<T, bool>
{
    bool operator()(cosnt T &x) const { return !x; }
};
```

这些仿函数所产生的对象，用法和一般函数完全相同。当然，我们也可以产生一个无名的临时对象来履行函数功能，例如：

```c++
#include <functional>
#include <iostream>
using namespace std;
int main()
{
    // 以下产生一些仿函数实体（对象）
    plus<int> plusobj;
    modulus<int> modulusobj;

    equal_to<int> equal_to_obj;
    greater_equal<int> greater_equal_obj;

    logical_and<int> logical_and_obj;

    // 以下运用上述对象，履行函数功能
    cout << plusobj(3, 5) << endl;    // 8
    cout << modulusobj(3, 5) << endl; // 3

    cout << equal_to_obj(3, 5) << endl;      // 0
    cout << greater_equal_obj(5, 3) << endl; // 1

    cout << logical_and_obj(true, true) << endl; // 1

    // 以下直接以仿函数的临时对象履行函数功能
    // 语法分析：function<T>()是一个临时对象，后面接一对小括号代表参数
    cout << plus<int>()(3, 5) << endl;    // 8
    cout << modulus<int>()(3, 5) << endl; // 3

    cout << equal_to<int>()(3, 5) << endl;      // 0
    cout << greater_equal<int>()(5, 3) << endl; // 1

    cout << logical_and<int>()(true, true) << endl; // 1
}
```

一般而言，不会有人在这么单纯的情况下运用这些功能及其简单的仿函数。仿函数的主要用途是为了搭配STL算法