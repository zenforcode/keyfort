# Base image with common tools
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install Go
ENV GOLANG_VERSION=1.21.5
RUN curl -sSL "https://go.dev/dl/go${GOLANG_VERSION}.linux-amd64.tar.gz" | tar -C /usr/local -xz \
    && ln -s /usr/local/go/bin/go /usr/local/bin/go \
    && ln -s /usr/local/go/bin/gofmt /usr/local/bin/gofmt

RUN mkdir -p /var/lib/foundationdb

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    && apt-get clean

# Install Node.js (for Reveal.js)
ENV NODE_VERSION=20
RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash - \
    && apt-get install -y nodejs wget\
    && npm install -g npm

# Install Java (required for Keycloak if needed)
RUN apt-get update && apt-get install -y openjdk-17-jdk wget unzip && apt-get clean
# Install FoundationDB CLI
RUN wget https://github.com/apple/foundationdb/releases/download/7.1.27/foundationdb-clients_7.1.27-1_amd64.deb
RUN dpkg -i foundationdb-clients_7.1.27-1_amd64.deb && rm foundationdb-clients_7.1.27-1_amd64.deb

# Create a non-root user
ARG USERNAME=vscode
WORKDIR "/home/${USERNAME}"
