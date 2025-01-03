---
sidebar_position: 1
---

# KeyFort: A secret storage

## Overview
The KeyFort Server is a secure, centralized solution for managing and storing sensitive data such as API keys, credentials, tokens, and other secrets. This server is designed with encryption, access control, and auditing features to ensure data security and compliance with industry standards.

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
  - Python 3.11+
  - FoundationDB (for backend storage)

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/zenforcode/keyfort
   cd keyfort
   ```

2. **Set up a virtual environment**:
   ```bash
   pip install uv
   uv venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Configure the environment**:
   - Copy the `.env.example` file and rename it to `.env`.
   - Update the configuration in `.env`:
     - Database connection string
     - Secret key for encryption
     - Other environment variables


5. **Start the server**:
   ```bash
   make run
   ```

## Configuration
All configurations are managed through the `.env` file. Key settings include:
- `DB_CONNECTION`: Database connection string (e.g., `mongodb://localhost:27017/keyvault` or `postgresql://user:password@localhost/keyvault`)
- `TOKEN_API_KEY`: Encryption key for securing data.
- `API_PORT`: Port number for the server.
- `LOG_LEVEL`: Logging verbosity (e.g., DEBUG, INFO, WARNING).

## Usage
### Adding a Secret
To add a secret, use the `/secrets` API endpoint:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"key": "api-key", "value": "12345"}' http://localhost:8080/secrets
```

### Retrieving a Secret
To retrieve a secret, use the `/secrets/{key}` endpoint:
```bash
curl -X GET http://localhost:8080/secrets/yoursecret
```

### Deleting a Secret
To delete a secret, use the `/secrets/{key}` endpoint:
```bash
curl -X DELETE http://localhost:8080/secrets/api-key
```

## Security
- **Encryption**: All secrets are encrypted at rest using AES-256.
- **Authentication**: Supports API key or JWT-based authentication for API access.
- **Authorization**: Role-based access control ensures only authorized users can perform specific actions.
- **Auditing**: All actions are logged for monitoring and auditing purposes.

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