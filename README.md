# ChatServer

**TCP Chat Server Using Socket Programming**  
CS381: Computer Networks – Final Project

## Overview

This project implements a multi-client chat server using TCP socket programming in Python. Clients connect to a central server and exchange messages with all other connected users through a client/server architecture. The project was completed as a solo final project for a computer networks course.

## Features

- Client/server model with separate scripts for each
- Concurrent support for multiple connected clients
- TCP sockets for reliable message delivery
- RSA-based message encryption and decryption
- Chat logs written to a local file on the client side

## Technical Details

- Language: Python  
- Core libraries: `socket`, `threading`, `rsa`, `tkinter`, `datetime`, `time`  
- Communication: TCP sockets  
- Encryption: RSA (512-bit key used for performance in a non-production setting)

Messages are encrypted before transmission and decrypted upon receipt. The server manages client connections and message broadcasting, while the client provides a simple user interface for sending and receiving messages.

## Usage

1. Start the server:
```bash
python server.py
```
2. Start one or more clients:
```bash
python client.py
```

Clients can connect simultaneously and participate in the shared chat session.

### Known Limitations
- No enforcement of unique usernames
- Encryption key size reduced for performance
- No private messaging or file transfer features
