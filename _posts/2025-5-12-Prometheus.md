---
title: Prometheus
author: zhugenmi
date: 2025-5-12 9:00 +0800
categories: [Systematic Capacity,TOOLS]
tags: [prometheus]
description: 
---
## Prometheus

[Prometheus](https://prometheus.io/docs/introduction/overview/) 是一个开源系统监控和警报工具包，最初由 SoundCloud 开发。自 2012 年推出以来，许多公司和组织都采用了 Prometheus，该项目拥有一个非常活跃的开发者和用户社区。现在，它是一个独立的开源项目，独立于任何公司进行维护。为了强调这一点，并明确项目的治理结构，Prometheus 于 2016 年加入了云原生计算基金会，成为继 Kubernetes 之后的第二个托管项目。

Prometheus 以时间序列数据的形式收集和存储其指标，即指标信息与记录时的时间戳以及称为标签的可选键值对一起存储。

## 特点

Prometheus 的主要特点包括：

- 多维数据模型，时间序列数据由度量名称和键/值对标识
- PromQL，一种灵活的查询语言，可充分利用这种多维性
- 不依赖分布式存储；单个服务器节点是独立的
- 通过 HTTP 上的拉模式收集时间序列
- 通过中间网关支持推送时间序列
- 通过服务发现或静态配置发现目标
- 支持多种模式的图表和仪表盘显示

## 指标

指标（metrics）是用通俗语言来说就是数字化的测量结果。时间序列这一术语指的是随时间推移记录的变化情况。不同应用场景中用户想测量的内容也各不相同：对于网络服务器，可能是请求耗时；对于数据库，可能是活跃连接数或正在执行的查询数量等等。

指标在理解应用程序运行状况方面起着关键作用。假设你运营着一个网页应用，突然发现运行变慢。要查明原因，你就需要获取相关信息。比如当请求量激增时，应用就可能出现延迟。如果拥有请求量这个指标，你就能锁定问题根源，进而通过增加服务器数量来应对流量压力。

## 组件

Prometheus 生态系统由多个组件构成，其中许多是可选的：

- Prometheus 主服务器：负责抓取并存储时间序列数据
- 客户端库：用于在应用代码中嵌入指标采集
- Push 网关：支持短期任务的指标推送
- 专用导出器：用于对接 HAProxy、StatsD、Graphite 等服务
- Alertmanager：负责告警管理
- 各类辅助工具

大多数 Prometheus 组件采用 Go 语言编写，因此可以轻松编译为静态二进制文件，便于部署。

## 架构

下图展示了 Prometheus 的架构及其生态系统的部分组件：![Prometheus architecture](../assets/img/sysCapacity/architecture.png)

Prometheus 会从已埋入监控指标的作业（jobs）中抓取指标数据，采集方式包括：

- 直接抓取（适用于常驻服务）
- 通过 Push 网关（适用于短期任务）

采集到的所有数据样本会本地存储，并通过预定义的规则进行计算：

- 聚合现有数据，生成新的时间序列
- 触发告警（例如当指标超过阈值时）

最终，采集的数据可通过 Grafana 或其他支持 Prometheus API 的工具进行可视化展示。

## **下载并运行 Prometheus**

### **1. 下载 Prometheus**

从官网下载[Download](https://prometheus.io/download)适用于主机平台的最新版本，并解压：

```shell
tar xvfz prometheus-*.tar.gz
cd prometheus-*
```

Prometheus 服务器是一个名为 `prometheus`（Windows 下为 `prometheus.exe`）的二进制文件。运行以下命令查看帮助选项：

```shell
./prometheus --help
```

------

### **2. 配置 Prometheus**

Prometheus 的配置文件采用 **YAML** 格式。解压后的目录中包含一个示例配置文件 `prometheus.yml`，精简后如下：

```yaml
global:
  scrape_interval:     15s  # 全局抓取间隔
  evaluation_interval: 15s  # 规则评估间隔

rule_files:            # 规则文件（暂无）
  # - "first.rules"
  # - "second.rules"

scrape_configs:
  - job_name: prometheus    # 监控 Prometheus 自身
    static_configs:
      - targets: ['localhost:9090']  # 监控目标地址
```

- **`global`**：全局配置，如抓取间隔（`scrape_interval`）和规则评估频率（`evaluation_interval`）。

- **`rule_files`**：告警或记录规则的引用文件（当前未启用）。

- **`scrape_configs`**：定义监控目标。默认配置监控 Prometheus 自身的 `/metrics` 端点（`http://localhost:9090/metrics`）。

> 提示：更多配置选项详见 [官方配置文档](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)。

------

### **3. 启动 Prometheus**

进入 Prometheus 目录，运行以下命令启动：

```shell
./prometheus --config.file=prometheus.yml
```

启动后访问以下地址：

- **状态页面**：`http://localhost:9090`（等待约 30 秒采集数据）
- **指标端点**：`http://localhost:9090/metrics`（查看 Prometheus 自身的监控数据）

------

### **4. 使用表达式浏览器**

访问 `http://localhost:9090/graph`，切换到 **"Table"** 视图，输入以下表达式查询指标：

- **示例 1**：查看所有请求状态的指标

  ```shell
  promhttp_metric_handler_requests_total
  ```

- **示例 2**：筛选 HTTP 状态码为 200 的请求

  ```shell
  promhttp_metric_handler_requests_total{code="200"}
  ```

- **示例 3**：统计返回的时间序列数量

  ```shell
  count(promhttp_metric_handler_requests_total)
  ```

------

### **5. 绘制指标图表**

在 `http://localhost:9090/graph` 的 **"Graph"** 选项卡中，输入以下表达式绘制每秒 HTTP 200 请求率：

```shell
rate(promhttp_metric_handler_requests_total{code="200"}[1m])
```

可通过调整时间范围和图形参数进行交互分析。

------

### **6. 扩展监控目标**

仅监控 Prometheus 自身无法体现其全部能力，建议通过 **Exporter** 监控其他服务。

**推荐入门**：参考 [监控 Linux/macOS 主机指标（使用 Node Exporter）](https://prometheus.io/docs/guides/node-exporter/) 文档。

## 使用 Node Exporter 监控 Linux 主机指标

### **1. 安装并运行 Node Exporter**

Node Exporter 是一个静态二进制文件，可通过以下步骤安装（[Download](https://github.com/prometheus/node_exporter/releases/download/v1.9.1/node_exporter-1.9.1.linux-amd64.tar.gz)）：

```shell
# 下载并解压（替换<VERSION>、<OS>和<ARCH>为实际值）
wget https://github.com/prometheus/node_exporter/releases/download/v<VERSION>/node_exporter-<VERSION>.<OS>-<ARCH>.tar.gz
tar xvfz node_exporter-*.*-amd64.tar.gz
cd node_exporter-*.*-amd64
./node_exporter
```

运行后输出类似以下内容，表示 Node Exporter 已在端口 `9100` 暴露指标：

```shell
INFO[0000] Listening on :9100  source="node_exporter.go:111"
```

------

### **2. 验证指标暴露**

通过 `curl` 检查指标是否正常生成：

```shell
curl http://localhost:9100/metrics
```

输出示例（含 `node_` 前缀的系统指标）：

```shell
# HELP node_cpu_seconds_total CPU 时间统计（单位：秒）
# TYPE node_cpu_seconds_total counter
node_cpu_seconds_total{cpu="0",mode="idle"} 10000.45
node_cpu_seconds_total{cpu="0",mode="system"} 50.12
...
```

筛选系统指标：

```shell
curl http://localhost:9100/metrics | grep "node_"
```

------

### **3. 配置 Prometheus 抓取 Node Exporter**

修改 Prometheus 配置文件 `prometheus.yml`，添加以下内容：

```shell
global:
  scrape_interval: 15s  # 全局抓取间隔

scrape_configs:
  - job_name: node      # 任务名称
    static_configs:
      - targets: ['localhost:9100']  # Node Exporter 地址
```

启动 Prometheus：

```shell
./prometheus --config.file=./prometheus.yml
```

------

### **4. 在 Prometheus 表达式中浏览指标**

访问 `http://localhost:9090/graph`，在表达式输入栏尝试以下查询：

| **指标表达式**                                    | **含义**                                              |
| :------------------------------------------------ | :---------------------------------------------------- |
| `rate(node_cpu_seconds_total{mode="system"}[1m])` | 过去一分钟内，每秒平均消耗在系统模式的 CPU 时间（秒） |
| `node_filesystem_avail_bytes`                     | 非 root 用户可用的文件系统空间（字节）                |
| `rate(node_network_receive_bytes_total[1m])`      | 过去一分钟内，每秒平均接收的网络流量（字节）          |

**示例操作**：

- 输入 `node_memory_MemAvailable_bytes` 查看可用内存。
- 使用 `rate(node_network_transmit_bytes_total[5m])` 计算 5 分钟平均网络发送速率。

- **CPU 使用率**：

  ```shell
  100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) by (instance) * 100)
  ```

- **磁盘剩余空间百分比**：

  ```shell
  (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100
  ```

> **提示**：更多指标详见 [Node Exporter 官方文档](https://prometheus.io/docs/guides/node-exporter/)。

------

## 系统典型指标说明及获取方法

1. **`cpu_usage_total`**

   - **含义**：容器总CPU使用率（%）。

   - **查询公式**：

     ```bash
     sum(rate(container_cpu_usage_seconds_total{namespace="train-ticket",pod="ts-ui-dashboard-f596f9f5c-f4z7r"}[1m])) * 100	
     ```
   
4. **`memory_usage`**

   - **含义**：容器内存使用量（字节，MB），含缓存。

   - **查询公式**：

     ```bash
     container_memory_usage_bytes{namespace="train-ticket", pod="ts-ui-dashboard-f596f9f5c-f4z7r"}/1048576
     ```

5. **`memory_working_set`**

   - **含义**：容器工作集内存（实际活跃使用的内存，字节，MB），常驻内存，排除缓存。

   - **查询公式**：

     ```bash
     container_memory_working_set_bytes{namespace="train-ticket",pod="ts-ui-dashboard-f596f9f5c-f4z7r"} /1048576
     ```

6. **`rx_bytes`**

   - **含义**：网络接收速率（KB/s）。

   - **查询公式**：

     ```bash
     rate(container_network_receive_bytes_total{namespace="train-ticket", pod="ts-ui-dashboard-f596f9f5c-f4z7r"}[3m]) / 1024
     ```

7. **`tx_bytes`**

   - **含义**：网络发送速率（KB/s）。

   - **查询公式**：

     ```bash
     rate(container_network_transmit_bytes_total{namespace="train-ticket", pod="ts-ui-dashboard-f596f9f5c-f4z7r"}[3m]) / 1024
     ```

语法格式见 [Prometheus监控入门之PromQL表达式语法学习](https://cloud.tencent.com/developer/article/2129817)。

官方文档：[Prometheus-Overview](https://prometheus.io/docs/introduction/overview/)
