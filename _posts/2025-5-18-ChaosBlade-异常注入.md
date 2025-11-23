---
title: ChaosBlade-异常注入
author: zhugenmi
date: 2025-5-18 10:00 +0800
categories: [Systematic Capacity,TOOLS]
tags: [chaosblade]
description: 
---

## 简介

[ChaosBlade](https://chaosblade.io/docs/) 是阿里巴巴 2019 年开源的混沌工程项目，包含混沌工程实验工具 chaosblade 和混沌工程平台 chaosblade-box，旨在通过混沌工程帮助企业解决云原生过程中高可用问题。实验工具 chaosblade 支持 3 大系统平台，4 种编程语言应用，共涉及 200 多种实验场景，3000 多个实验参数，可以精细化的控制实验范围。 混沌工程平台 chaosblade-box 支持实验工具托管，除已托管 chaosblade 外，还支持 Litmuschaos 实验工具。

ChaosBlade 支持多种环境部署与演练，包括 linux、docker、kubernetes 集群及各类云厂商环境。ChaosBlade 主要包括以下几个组件：

- ChaosBlade-Box Console：ChaosBlade 可视化组件，主要提供一套用户友好的 Web 界面，用户可以通过该界面进行混沌工程实验的编排与操作管理。
- ChaosBlade-Box Server：核心逻辑组件，主要负责混沌工程实验的管理与编排，探针与应用管理。包括组件，Chaos Engine：演练引擎，包括流程编排、安全管控、演练报告等功能；Chaos Runner：演练执行器，兼容多种执行工具；Chaos Experience：演练经验库等。
- Agent：核心逻辑组件，部署在用户终端的主机或 Kubernetes 集群内，主要负责和 ChaosBlade-Box Server 建联上报心跳并作为命令下发通道。
- ChaosBlade：主要执行工具，能在主机和 Kubernetes 等不同环境上执行故障注入，能对系统网络设备、文件系统、内核及系统上运行的应用等进行故障干扰。

## ChaosBlade-Box  平台安装与卸载

### 环境准备

具体环境准备参见：k8s集群搭建

### 使用 Helm 安装

第一步，下载 Box Chart 包

查看所有可以下载的 [box-release](https://github.com/chaosblade-io/chaosblade-box/releases)，下载到本地，如：

```shell
wget https://github.com/chaosblade-io/chaosblade-box/releases/download/v1.0.2/chaosblade-box-1.0.2.tgz
```

第二步，进行安装

```shell
root@k8s-master:~/work# helm install chaosblade-box chaosblade-box-1.0.2.tgz --namespace chaosblade --set spring.datasource.password=DATASOURCE_PASSWORD
NAME: chaosblade-box
LAST DEPLOYED: Mon Jul 14 11:25:11 2025
NAMESPACE: chaosblade
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Thank you for using chaosblade-box.
```

等待Pods就绪：

```bash
Croot@k8s-master:~/work# kubectl get po -n chaosblade 
NAME                                    READY   STATUS    RESTARTS       AGE
chaosblade-box-678c848b5f-8fdxx         1/1     Running   2 (111s ago)   3m4s
chaosblade-box-mysql-79fd97f685-nc7zs   1/1     Running   0              3m4s
```

### 验证安装

要查看 Box 运行情况，请执行以下命令：

```shell
kubectl get po -n chaosblade
```

以下是预期输出

```shell
NAME                                    READY   STATUS    RESTARTS   AGE
chaosblade-box-5bc47b676f-2gjh9         1/1     Running   0          15d
chaosblade-box-mysql-58cc864896-2jxrs   1/1     Running   0          15d
```

如果你的实际输出与预期输出相符，表示 ChaosBlade-Box 已经安装成功。

```shell
# 以chaosblade-box为例
kubectl describe po chaosblade-box-5bc47b676f-2gjh9 -n chaosblade
```

### 卸载 ChaosBlade-Box

如果需要卸载 ChaosBlade-Box，请执行以下命令：

```shell
helm un chaosblade-box -n chaosblade
```

##  ChaosBlade 工具安装与卸载

### 环境准备

具体环境准备参见：k8s集群构建

### 使用 Helm 安装

```shell
helm repo add chaosblade-io https://chaosblade-io.github.io/charts
helm install chaosblade chaosblade-io/chaosblade-operator --namespace chaosblade
```

### 验证安装

要查看 Box 运行情况，请执行以下命令：

```shell
kubectl get po -n chaosblade
```

以下是预期输出

```shell
NAME                                    READY   STATUS    RESTARTS   AGE
chaosblade-operator-688568959-lcwgb     1/1     Running   0          6s
chaosblade-tool-c9xjd                   1/1     Running   0          6s
chaosblade-tool-hvqcv                   1/1     Running   0          6s
chaosblade-tool-q8jjd                   1/1     Running   0          6s
```

如果你的实际输出与预期输出相符，表示 ChaosBlade-Box 已经安装成功。

```shell
# 以chaosblade-operator为例
kubectl describe po chaosblade-operator-688568959-lcwgb -n chaosblade
```

### 卸载 ChaosBlade

如果需要卸载 ChaosBlade，请执行以下命令：

```shell
helm uninstall chaosblade-operator --namespace chaosblade
```

卸载后可在查看 crd 资源是否也已经删除：

```shell
kubectl get crds | grep chaos
```

如果 blade crd 资源还存在可通过以下命令进行删除：

```shell
kubectl delete crd chaosblades.chaosblade.io
```

如果 crd 资源删除长时间没有成功，可通过以下命令进行删除：

```shell
blades=$(kubectl get blade | grep -v NAME | awk '{print $1}' | tr '\n' ' ') && kubectl patch blade $blades --type merge -p '{"metadata":{"finalizers":[]}}'
```

### 安装 chaosblade-operator时报错：**too many open files**



## 异常注入

参考：https://chaosblade.io/docs/experiment-types/k8s/

安装 chaosblade operator 后即可执行混沌实验，执行方式有以下三种：

- 通过配置 yaml 方式，使用 kubectl 执行
- 使用 chaosblade cli 工具执行
- 通过编写代码调用 Kubernetes API 执行

这里选择通过配置yaml的方式。

### 模拟资源不足

指定节点，模拟CPU负载90%的实验，制造资源不足的异常场景。

```yaml
apiVersion: chaosblade.io/v1alpha1
kind: ChaosBlade
metadata:
  name: cpu-load
spec:
  experiments:
    - scope: node
      target: cpu
      action: fullload
      desc: "increase node cpu load by names"
      matchers:
        - name: names
          value:
            - "192.168.31.102"
        - name: cpu-percent
          value:
            - "90"
```

配置好文件后，保存为 chaosblade_cpu_load.yaml，使用以下命令执行实验场景：

```bash
kubectl apply -f chaosblade_cpu_load.yaml
```

查看实验状态：

```bash
kubectl get blade cpu-load -o json
```

销毁实验：

```bash
kubectl delete chaosblade cpu-load # 根据实验资源名
kubectl delete -f chaosblade_cpu_load.yaml # 根据yaml配置文件
blade destroy <UID> # 通过blade命令
# UID 是执行 blade create 命令返回的结果，如果忘记，可使用 blade status --type create 命令查询
```

### 模拟网络延迟

在train-ticket命名空间下，指定名为ts-wait-order-service-779cc799d5-hmz8g的Pod本地端口32677 访问延迟 2000毫秒，延迟时间上下浮动1000毫秒：

```yaml
apiVersion: chaosblade.io/v1alpha1
kind: ChaosBlade
metadata:
  name: delay-pod-network
spec:
  experiments:
    - scope: pod
      target: network
      action: delay
      desc: "delay pod network by names"
      matchers:
        - name: names
          value:
            - "ts-wait-order-service-779cc799d5-hmz8g"
        - name: namespace
          value:
            - "train-ticket"
        - name: local-port
          value: ["32677"]
        - name: interface
          value: ["ens33"]
        - name: time
          value: ["2000"]
        - name: offset
          value: ["1000"]
```

保存为 yaml 文件，比如 chaosblade_delay_pod_network.yaml，使用 kubectl 命令执行：

```text
kubectl apply -f chaosblade_delay_pod_network.yaml
```

停止实验：

```sh
kubectl delete -f chaosblade_delay_pod_network.yaml
```

### 模拟网络丢包

模拟192.168.31.102节点本地端口32677 80%的网络丢包：

```yaml
apiVersion: chaosblade.io/v1alpha1
kind: ChaosBlade
metadata:
  name: loss-node-network
spec:
  experiments:
  - scope: node
    target: network
    action: loss
    desc: "node network loss"
    matchers:
    - name: names
      value: ["192.168.31.102"]
    - name: percent
      value: ["90"]
    - name: interface
      value: ["ens33"]
    - name: local-port
      value: ["32677"]
```

执行实验：

```bash
kubectl apply -f chaosblade_loss_node_network.yaml
```

查看实验状态：

```bash
kubectl get blade loss-node-network -o json 
```

停止实验：

```bash
kubectl delete -f chaosblade_loss_node_network.yaml
```

或者直接删除此blade 资源：

```bash
kubectl delete blade loss-node-network
```

