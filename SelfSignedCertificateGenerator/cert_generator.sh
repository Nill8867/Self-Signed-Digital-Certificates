#!/bin/bash

# CNS Digital Certificate Generator
# This script generates RSA keys and self-signed certificates for TLS communication

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create directories if they don't exist
mkdir -p certs
mkdir -p config

# Check if OpenSSL is installed
if ! command -v openssl &> /dev/null; then
    echo -e "${RED}Error: OpenSSL is not installed or not in PATH${NC}"
    echo "Please install OpenSSL and try again"
    exit 1
fi

# Default validity period (days)
VALIDITY=365

# Check if user provided a validity period
if [ $# -eq 1 ] && [[ $1 =~ ^[0-9]+$ ]]; then
    VALIDITY=$1
    echo -e "${BLUE}Setting certificate validity to $VALIDITY days${NC}"
fi

# Check if openssl.cnf exists
if [ ! -f "config/openssl.cnf" ]; then
    echo -e "${YELLOW}Warning: config/openssl.cnf not found${NC}"
    echo "Creating default OpenSSL configuration file..."
    
    cat > config/openssl.cnf << 'EOL'
# OpenSSL configuration for CNS Digital Certificate Generator

[ req ]
default_bits       = 2048
default_keyfile    = server.key
distinguished_name = req_distinguished_name
req_extensions     = v3_req
prompt             = no

[ req_distinguished_name ]
C  = US
ST = California
L  = San Francisco
O  = CNS Educational Project
OU = Computer Network Security
CN = localhost

[ v3_req ]
basicConstraints     = CA:FALSE
keyUsage             = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage     = serverAuth, clientAuth
subjectAltName       = @alt_names

[ alt_names ]
DNS.1 = localhost
IP.1 = 127.0.0.1
EOL

    echo -e "${GREEN}Created config/openssl.cnf${NC}"
fi

echo -e "\n${BLUE}=== CNS Digital Certificate Generator ===${NC}"

# Generate RSA private key (2048 bits)
echo -e "\n${YELLOW}Step 1: Generating RSA private key (2048 bits)...${NC}"
openssl genrsa -out certs/server.key 2048
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to generate RSA private key${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Private key generated successfully: certs/server.key${NC}"

# Create Certificate Signing Request (CSR) using the config file
echo -e "\n${YELLOW}Step 2: Creating Certificate Signing Request (CSR)...${NC}"
openssl req -new -key certs/server.key -out certs/server.csr -config config/openssl.cnf
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to create Certificate Signing Request${NC}"
    exit 1
fi
echo -e "${GREEN}✓ CSR created successfully: certs/server.csr${NC}"

# Generate self-signed certificate
echo -e "\n${YELLOW}Step 3: Generating self-signed certificate (valid for $VALIDITY days)...${NC}"
openssl x509 -req -days $VALIDITY -in certs/server.csr -signkey certs/server.key -out certs/server.crt -extensions v3_req -extfile config/openssl.cnf
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to generate self-signed certificate${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Self-signed certificate generated successfully: certs/server.crt${NC}"

# Verify the certificate
echo -e "\n${YELLOW}Step 4: Verifying certificate...${NC}"
echo -e "${BLUE}Certificate Information:${NC}"
openssl x509 -in certs/server.crt -text -noout | grep -E 'Subject:|Issuer:|Not Before:|Not After:|DNS:|IP Address:'
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to verify certificate${NC}"
    exit 1
fi

echo -e "\n${GREEN}=== Certificate Generation Completed Successfully! ===${NC}"
echo -e "Files generated:"
echo -e "  - ${BLUE}Private Key:${NC} certs/server.key"
echo -e "  - ${BLUE}CSR:${NC} certs/server.csr"
echo -e "  - ${BLUE}Certificate:${NC} certs/server.crt"
echo -e "\nTo run the TLS server: ${YELLOW}cd server && python tls_server.py${NC}"
echo -e "To run the TLS client: ${YELLOW}cd client && python tls_client.py${NC}"