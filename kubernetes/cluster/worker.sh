#! /bin/bash

# rdate time setting
yum install -y rdate
rdate -s time.bora.net

# /etc/hosts file edit
cat >> /etc/hosts << EOF
172.16.1.20	master
172.16.1.21	node1
172.16.1.22	node2
EOF

# firewall off & disable
systemctl stop firewalld
systemctl disable firewalld

# using linux kernel module 
modprobe overlay
modprobe br_netfilter

# overlay 및 iptables Module Load
cat > /etc/modules-load.d/k8s.conf << EOF
overlay
br_netfilter
EOF

# iptables & NAT on
cat > /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward =1
EOF
sysctl --system

# selinux off
setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux

# swap off
swapoff -a
sed -i '/swap/ s/^\(.*\)$/#\1/g' /etc/fstab

cat /etc/fstab
swapon -s 

#uninstall docker previous version
yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine

yum install wget -y
wget https://download.docker.com/linux/centos/docker-ce.repo -O /etc/yum.repos.d/docker-ce.repo
yum install -y containerd.io

containerd config default > /etc/containerd/config.toml
systemctl start containerd && systemctl enable containerd
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
sed -i \
 's,config_path = \"\",config_path = \"/etc/containerd/certs.d\",g' \
 /etc/containerd/config.toml

systemctl restart containerd 
systemctl enable --now containered

# K8S Repository 
cat <<EOF > /etc/yum.repos.d/kubernetes.repo

[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kube
EOF

yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
systemctl enable kubelet && systemctl start kubelet
