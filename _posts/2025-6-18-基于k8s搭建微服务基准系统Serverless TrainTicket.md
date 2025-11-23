---
title: 基于k8s搭建微服务基准系统Serverless TrainTicket
author: zhugenmi
date: 2025-6-18 11:00 +0800
categories: [Systematic Capacity,TOOLS]
tags: [k8s]
description: 
---

## Serverless TrainTicket 部署

TrainTicket 是复旦大学 CodeWisdom 团队按照工业界微服务实践所开发的一个开源微服务基准系统，是基于微服务架构的一个火车订票系统，包含了 41 种微服务。本项目使用开源函数计算框架 OpenFaaS、基于 Serverless 架构提取并改造开源微服务系统 TrainTicket 中高并发的订票业务，部署并运行在 Kubernetes 集群中。主要使用的开发技术框架如下： Java - OpenFaaS、OkHttp、*Spring Boot DB - MongoDB、MongoBD JDBC。地址：https://github.com/FudanSELab/serverless-trainticket

### 1. 安装  OpenFaaS

```bash
# 创建命名空间
kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml

# 添加 OpenFaaS chart 仓库
helm repo update

# 安装 OpenFaaS（使用 containerd 兼容配置）
helm upgrade openfaas --install openfaas/openfaas \
    --namespace openfaas \
    --set functionNamespace=openfaas-fn \
    --set generateBasicAuth=true \
    --set openfaasImagePullPolicy=IfNotPresent
```

### 2. 配置 OpenFaaS CLI

```bash
# 获取 admin 密码
PASSWORD=$(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode)

# 配置 CLI 凭证
echo $PASSWORD | faas-cli login -u admin --password-stdin

# 验证连接
faas-cli version
```

### 3. 准备项目环境

```bash
git clone https://github.com/GitHubDiom/serverless-trainticket
cd serverless-trainticket

# 下载 Java8 模板
wget https://github.com/openfaas/templates/archive/refs/tags/1.9.0.tar.gz
tar -zxvf 1.9.0.tar.gz
mv templates-1.9.0/template ./
rm -rf templates-1.9.0 1.9.0.tar.gz
```

接下来需要配置NFS共享文件目录，参考[配置NFS共享文件目录](./配置NFS共享文件目录.md)。

### 4. 设置环境变量

```bash
# 使用实际值替换
export MASTER_IP=192.168.1.100       # 替换为您的 master 节点 IP
export DOCKER_USERNAME=your_dockerhub_username
export NFS_PATH=/var/nfs/data        # 根据您的 NFS 挂载路径调整
```

### 5. 部署数据库

```bash
# 修改脚本适配 containerd
sed -i 's/docker/nerdctl/g' part01_DataBaseDeployment.sh

# 执行部署
chmod u+x part01_DataBaseDeployment.sh
./part01_DataBaseDeployment.sh

# 等待 Pods 就绪
kubectl get pods -w --namespace=default
```

### 6. 初始化数据

```bash
chmod u+x part01_DataInitiation.sh
./part01_DataInitiation.sh
```

### 7. 部署后端服务

```bash
# 适配 containerd 的镜像构建
find . -name "*.sh" -exec sed -i 's/docker build/nerdctl build/g' {} \;

# 部署 BaaS
chmod u+x part02_BaaSServices.sh
./part02_BaaSServices.sh

# 部署 FaaS
chmod u+x part02_FaaSFunctions.sh
./part02_FaaSFunctions.sh
```

### 8. 部署前端

```bash
chmod u+x part03_Frontend.sh
./part03_Frontend.sh
```

### 9. 验证部署

```bash
# 检查所有 Pods 状态
kubectl get pods --all-namespaces -w

# 获取前端访问地址
NODE_PORT=$(kubectl get svc frontend -o jsonpath='{.spec.ports[0].nodePort}')
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')

echo "访问地址: http://$NODE_IP:$NODE_PORT"
```
