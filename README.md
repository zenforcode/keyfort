# KeyFort (WIP)
## Overview
The KeyFort Server is a secure, centralized solution for managing and storing sensitive data such as API keys, credentials, tokens, and other secrets. This server is designed with encryption, access control, and auditing features to ensure data security and compliance with industry standards.

## Architecture

```mermaid
graph TD

  subgraph Client
    A[REST API Client]
  end

  subgraph Keyfort
    B[REST API Server]

    B1[Authenticate]
    B2[GetSecret]
    B3[SetSecret]
    B4[Tokenize]
    B5[Encipher]

    B6[IdentityService]
    B7[CryptoService]
    B8[SecretService]
  end

  subgraph CloudProviders
    C1[Azure Identity Provider]
    C2[AWS Identity Provider]
  end

  subgraph HSMs
    D1[SoftHSM]
    D2[AWS/Azure HSM]
  end

  subgraph Storage
    E[FoundationDB]
  end

  %% Client to API
  A --> B

  %% API ops
  B --> B1
  B --> B2
  B --> B3
  B --> B4
  B --> B5

  %% IdentityService
  B1 --> B6
  B2 --> B6
  B3 --> B6
  B4 --> B6
  B5 --> B6

  B6 --> C1
  B6 --> C2

  %% CryptoService
  B2 --> B7
  B3 --> B7
  B4 --> B7
  B5 --> B7

  B7 --> D1
  B7 --> D2

  %% SecretService
  B2 --> B8
  B3 --> B8

  B8 --> E
```

## Features
- **Secure Storage**: Encrypts all stored data with robust encryption algorithms.
- **Access Control**: Role-based access control (RBAC) for managing user permissions.
- **Audit Logs**: Tracks and records all actions and access events for security auditing.
- **API Access**: Provides a RESTful API for integration with applications and services.
- **Versioning**: Maintains version history of secrets for rollback and audit purposes.
- **Expirable Secrets**: Supports time-limited secrets that automatically expire after a set duration.

## Prerequisites
Before setting up the KeyVault Server, ensure the following:
- **Operating System**: Linux (preferred), macOS, or Windows.
- **Dependencies**:
  - Go lang
  - FoundationDB (for backend storage)

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/zenforcode/keyfort
   cd keyfort
   ```

2. **Install the linter**:
  ```bash
  curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/HEAD/install.sh | sh -s -- -b $(go env GOPATH)/bin v2.0.2
  golangci-lint --version
  ```
3. **Build**:
   ```bash
  make
   ```


4. **Start the server**:
   ```bash
   make run
   ```

## Configuration
All configurations are managed through the `.env` file. Key settings include:
- `DB_CONNECTION`: Database connection string (e.g., `mongodb://localhost:27017/keyvault` or `postgresql://user:password@localhost/keyvault`)
- `TOKEN_API_KEY`: Encryption key for securing data.
- `API_PORT`: Port number for the server.
- `LOG_LEVEL`: Logging verbosity (e.g., DEBUG, INFO, WARNING).


## Testing
Run unit tests to ensure the application is functioning as expected:
```bash
make test
```

## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature/name`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For questions or support, contact the maintainer at [team@zenforcode.com](mailto:team@zenforcode.com).
