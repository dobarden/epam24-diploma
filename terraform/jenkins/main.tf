terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  required_version = "~> 1.0"
}

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.aws_region
}


#------------------VPC-----------------

resource "aws_vpc" "terraform-vpc" {
  cidr_block           = "10.1.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "Diploma_Jenkins_VPC"
  }
}

resource "aws_subnet" "subnet1" {
  vpc_id     = aws_vpc.terraform-vpc.id
  cidr_block = "10.1.10.0/24"

  tags = {
    Name = "Diploma_Jenkins_Subnet"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.terraform-vpc.id

  tags = {
    Name = "Diploma_Jenkins_IGW"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.terraform-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "Diploma_Jenkins_Route_Table"
  }
}

resource "aws_route_table_association" "public1" {
  subnet_id      = aws_subnet.subnet1.id
  route_table_id = aws_route_table.public.id
}


#------------------SG--------------------

resource "aws_security_group" "jenkins-sg" {
  name   = "Diploma_Jenkins_SG"
  vpc_id = aws_vpc.terraform-vpc.id
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
    ingress {
    from_port   = 9000
    to_port     = 9000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "Diploma_Jenkins_SG"
  }
}

resource "aws_security_group" "efs-sg" {
  name   = "Diploma_Jenkins_EFS_SG"
  vpc_id = aws_vpc.terraform-vpc.id

  ingress {
    from_port   = 2049
    to_port     = 2049
    protocol    = "tcp"
    cidr_blocks = ["10.1.10.0/24"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["10.1.10.0/24"]
  }

  tags = {
    Name = "Diploma_Jenkins_EFS_SG"
  }
}


#------------------EFS--------------------

resource "aws_efs_file_system" "JenkinsEFS" {
  tags = {
    Name = "Diploma_Jenkins_EFS"
  }
}

resource "aws_efs_mount_target" "efs-mount-1" {
  file_system_id  = aws_efs_file_system.JenkinsEFS.id
  subnet_id       = aws_subnet.subnet1.id
  security_groups = [aws_security_group.efs-sg.id]
}


#------------------EC2--------------------

resource "aws_instance" "jenkins_server" {
  ami                         = "ami-064ff912f78e3e561"
  instance_type               = "t3.medium"
  key_name                    = "ohio1"
  vpc_security_group_ids      = [aws_security_group.jenkins-sg.id]
  subnet_id                   = aws_subnet.subnet1.id
  associate_public_ip_address = true
  user_data                   = <<-EOF
              #!/bin/bash
              yum update -y
              yum install amazon-linux-extras -y
              yum install amazon-efs-utils -y
              amazon-linux-extras install java-openjdk11 -y
              wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
              rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
              yum update
              yum install jenkins -y
              systemctl start jenkins
              systemctl enable jenkins
              #mkdir -p /var/lib/jenkins
              mount -t efs -o tls ${aws_efs_file_system.JenkinsEFS.id}:/ /var/lib/jenkins
              echo "${aws_efs_file_system.JenkinsEFS.id}:/ /var/lib/jenkins efs defaults,_netdev 0 0" >> /etc/fstab
              chown -R jenkins:jenkins /var/lib/jenkins
              yum install docker -y
              systemctl start docker
              systemctl enable docker
              usermod -a -G docker jenkins
              systemctl restart jenkins
              yum install git -y
              curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl \
              -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
              chmod +x ./kubectl
              mv ./kubectl /usr/bin
              curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 > get_helm.sh
              chmod 700 get_helm.sh
			  ./get_helm.sh
              mv /usr/local/bin/helm /usr/bin
              aws configure set default.region ${var.aws_region}
              aws configure set aws_access_key_id '${var.aws_access_key}'
              aws configure set aws_secret_access_key '${var.aws_secret_key}'
              aws eks update-kubeconfig --region us-east-2 --name diploma-cluster
              mv ~/.aws/ /var/lib/jenkins/
              chown -R jenkins: /var/lib/jenkins/.aws/
              EOF
  tags = {
    Name = "Diploma_Jenkins_Server"
  }

  depends_on = [aws_efs_mount_target.efs-mount-1]
}

