# CNS Digital Certificate Generator with TLS Client-Server

This project demonstrates how to generate digital certificates and implement a secure TLS connection between a client and server. It's designed for students learning Computer and Network Security (CNS) concepts.

## Features

- Generate RSA private keys (2048 bits)
- Create Certificate Signing Requests (CSR) with proper configuration
- Generate self-signed X.509 certificates with configurable validity period
- Support for Subject Alternative Names (localhost and 127.0.0.1)
- Extended key usage for both server and client authentication
- Secure TLS server implementation with Python's built-in ssl module
- TLS client with certificate verification capabilities
- Interactive messaging between client and server
- Comprehensive error handling and user guidance

### Enhanced Features

- **Interactive Terminal UI**
  - Curses-based user interface for both client and server
  - Color-coded messages for better readability
  - Scrollable message history
  - Clean input handling

- **Multi-Client Support**
  - Server handles multiple clients simultaneously
  - Broadcast messaging system
  - Client connection status updates
  - Message history per client

- **Robust Error Handling**
  - Automatic reconnection attempts for clients
  - Graceful connection termination
  - Certificate validation
  - Comprehensive error messages

- **Real-time Communication**
  - Instant message broadcasting
  - Connection status notifications
  - Message timestamps
  - Last 100 messages history per client

## Project Structure

```
cns_cert_generator/
├── certs/                     # Output folder for certificates and keys
├── config/
│   └── openssl.cnf           # OpenSSL config file for cert generation
├── server/
│   └── tls_server.py         # TLS server using Python and SSL
├── client/
│   └── tls_client.py         # TLS client with UI
└── cert_generator.sh         # Bash script to generate certs
```

## Requirements

- OpenSSL (for certificate generation)
- Python 3.6+ (for TLS client and server)
- Terminal with curses support
- No external Python libraries required (uses built-in modules)

## Quick Start

1. **Generate Certificates**

```bash
npm run generate-certs
```

Or with custom validity:

```bash
npm run generate-certs -- 730  # Creates a certificate valid for 730 days
```

2. **Start the Server**

```bash
npm run start-server
```

3. **Start a Client**

```bash
npm run start-client
```

## Using the Interactive UI

### Server Interface
- Shows real-time connection status
- Displays incoming/outgoing messages
- Color-coded status messages
- Press Ctrl+C to shutdown

### Client Interface
- Green: Success messages and server responses
- Yellow: Status updates and warnings
- Red: Error messages
- Type 'exit' to disconnect
- Press Enter to send messages
- Scrollable message history

## Certificate Details

The generated certificate includes:

- **Subject Information**:
  - Country (C)
  - State/Province (ST)
  - Locality (L)
  - Organization (O)
  - Organizational Unit (OU)
  - Common Name (CN)

- **Key Usage Extensions**:
  - Digital Signature
  - Non-Repudiation
  - Key Encipherment

- **Extended Key Usage**:
  - Server Authentication
  - Client Authentication

- **Subject Alternative Names**:
  - DNS: localhost
  - IP: 127.0.0.1

## Learning Outcomes

By working with this project, students will learn:

- How digital certificates and Public Key Infrastructure (PKI) work
- The process of creating and signing X.509 certificates
- The role of Certificate Signing Requests (CSRs) in certificate issuance
- How TLS/SSL establishes secure network communications
- Certificate verification in secure communications
- Implementing secure client-server communications using Python
- Understanding key usage and extended key usage in certificates
- The importance of Subject Alternative Names (SANs)
- Building interactive terminal user interfaces
- Handling multiple client connections
- Implementing robust error handling
- Managing secure message broadcasting

## Security Notes

- The certificates generated are self-signed and should only be used for educational purposes
- In a production environment, certificates should be signed by a trusted Certificate Authority (CA)
- The private key should be kept secure and not shared
- This implementation focuses on educational clarity rather than production security best practices