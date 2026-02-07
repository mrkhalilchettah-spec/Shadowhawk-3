# Shadowhawk Core Deployment Guide

This guide describes how to deploy Shadowhawk Core on a standard Linux VPS.

## System Requirements
- OS: Ubuntu 22.04 LTS or 24.04 LTS
- CPU: 2+ Cores
- RAM: 4GB+
- Disk: 20GB+
- Software: Docker, Docker Compose

## Step-by-Step Installation

### 1. Install Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### 2. Clone and Configure
```bash
git clone https://github.com/shadowhawk-core/shadowhawk-core.git
cd shadowhawk-core
cp .env.example .env
# Edit .env with your preferred secrets and settings
nano .env
```

### 3. Launch the System
```bash
sudo docker-compose up -d
```

### 4. Verify Deployment
- API: `curl http://localhost:8000/health`
- Engine: `curl http://localhost:8080/health`

## Post-Deployment Checklist
- [ ] Change default database passwords in `.env`.
- [ ] Ensure `SECRET_KEY` is set to a long, random string.
- [ ] Configure firewall (UFW) to only allow ports 8000 (API) if external access is needed.
- [ ] Set up a reverse proxy (e.g., Nginx) with SSL if exposing to the internet.
