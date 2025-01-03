---
sidebar_position: 1
---

# KeyFort API Design

The Vault HTTP API gives you full access to Vault using REST like HTTP verbs. Every aspect of Vault can be controlled using the APIs. The Vault CLI uses the HTTP API to access Vault similar to all other consumers.

All API routes are prefixed with /v1/.

This documentation is only for the v1 API, which is currently the only version.

Backwards compatibility: At the current version, Vault does not yet promise backwards compatibility even with the v1 prefix. We'll remove this warning when this policy changes. At this point in time the core API (that is, sys/ routes) change very infrequently, but various secrets engines/auth methods/etc. sometimes have minor changes to accommodate new features as they're developed.
Transport

The API is expected to be accessed over a TLS connection at all times, with a valid certificate that is verified by a well-behaved client. It is possible to disable TLS verification for listeners, however, so API clients should expect to have to do both depending on user settings.
Authentication

Once Vault is unsealed, almost every other operation requires a client token. A user may have a client token sent to them. The client token must be sent as either the X-Vault-Token HTTP Header or as Authorization HTTP Header using the Bearer scheme.

Otherwise, a client token can be retrieved using an authentication engine.

Each auth method has one or more unauthenticated login endpoints. These endpoints can be reached without any authentication, and are used for authentication to Vault itself. These endpoints are specific to each auth method.

Responses from auth login methods that generate an authentication token are sent back to the client in JSON. The resulting token should be saved on the client or passed via the X-Vault-Token or Authorization header for future requests.
Parameter restrictions

Several Vault APIs require specifying path parameters. The path parameter cannot end in periods. Otherwise, Vault will return a 404 unsupported path error.

## Namespaces

When using Namespaces the final path of the API request is relative to the X-Vault-Namespace header. For instance, if a request URI is secret/foo with the X-Vault-Namespace header set as ns1/ns2/, then the resulting request path to Vault will be ns1/ns2/secret/foo.

Note that it is semantically equivalent to use the full path rather than the X-Vault-Namespace header, Vault will match the corresponding namespace based on correlating user input. Similar path results may be achieved if X-Vault-Namespace is set to ns1/ with the request path of ns2/secret/foo as well, or otherwise if X-Vault-Namespace is omitted entirely and instead a complete path is provided such as: ns1/ns2/secret/foo.

For example, the following two commands result in equivalent requests:
```bash
curl \
    -H "X-Vault-Token: f3b09679-3001-009d-2b80-9c306ab81aa6" \
    -H "X-Vault-Namespace: ns1/ns2/" \
    -X GET \
    http://127.0.0.1:8200/v1/secret/foo
```
```bash
curl \
    -H "X-Vault-Token: f3b09679-3001-009d-2b80-9c306ab81aa6" \
    -X GET \
    http://127.0.0.1:8200/v1/ns1/ns2/secret/foo
```
