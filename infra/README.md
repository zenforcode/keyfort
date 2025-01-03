1. Install AWS CLI
``bash
sudo apt-get install curl unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
``
2. Install Kubectl
``bash
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.31.2/2024-11-15/bin/linux/arm64/kubectl
chmod +x kubectl
sudo kubectl /usr/local/bin
``