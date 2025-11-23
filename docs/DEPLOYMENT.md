# Deployment Guide

This guide covers deploying Open Donation Tracker to production.

## Prerequisites

- Server with Docker and Docker Compose installed
- Domain name with DNS configured
- SSL certificate (Let's Encrypt recommended)

## Production Environment

### 1. Server Setup

#### Update System
```bash
sudo apt update && sudo apt upgrade -y
```

#### Install Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### Install Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Application Setup

#### Clone Repository
```bash
git clone https://github.com/yourusername/open-donation-tracker.git
cd open-donation-tracker
```

#### Configure Environment
```bash
cp .env.example .env
nano .env
```

Update the following variables:
```env
# Database
POSTGRES_USER=donationuser
POSTGRES_PASSWORD=<STRONG_PASSWORD>
POSTGRES_DB=donationtracker

# Backend
SECRET_KEY=<GENERATE_STRONG_KEY>
JWT_SECRET_KEY=<GENERATE_STRONG_KEY>
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.com

# Frontend
VITE_API_URL=https://api.yourdomain.com
```

Generate strong keys:
```bash
openssl rand -hex 32
```

### 3. SSL/TLS Setup with Let's Encrypt

#### Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

#### Obtain Certificate
```bash
sudo certbot certonly --standalone -d yourdomain.com -d api.yourdomain.com
```

### 4. Nginx Configuration

Create `/etc/nginx/sites-available/donation-tracker`:

```nginx
# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Frontend
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/donation-tracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Deploy Application

#### Build and Start Services
```bash
docker-compose build
docker-compose up -d
```

#### Initialize Database
```bash
docker-compose exec backend python -m app.init_db
```

#### Verify Deployment
```bash
docker-compose ps
docker-compose logs -f
```

### 6. Database Backups

#### Create Backup Script

Create `/opt/backup-donation-tracker.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/backups/donation-tracker"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

docker-compose exec -T postgres pg_dump -U donationuser donationtracker > $BACKUP_DIR/backup_$DATE.sql

# Keep only last 30 days
find $BACKUP_DIR -name "backup_*.sql" -mtime +30 -delete
```

Make executable:
```bash
chmod +x /opt/backup-donation-tracker.sh
```

#### Schedule Backups

Add to crontab:
```bash
crontab -e
```

Add line:
```
0 2 * * * /opt/backup-donation-tracker.sh
```

### 7. Monitoring

#### Setup Log Rotation

Create `/etc/logrotate.d/donation-tracker`:

```
/var/log/donation-tracker/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

#### Monitor Services

```bash
# View logs
docker-compose logs -f

# Check resource usage
docker stats

# Check service health
curl https://api.yourdomain.com/api/health
```

## Updating the Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose build
docker-compose up -d

# Run migrations if needed
docker-compose exec backend alembic upgrade head
```

## Scaling

### Horizontal Scaling

Use Docker Swarm or Kubernetes for horizontal scaling:

```yaml
# docker-compose.scale.yml
services:
  backend:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

### Load Balancing

Configure Nginx as load balancer:

```nginx
upstream backend_servers {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    location / {
        proxy_pass http://backend_servers;
    }
}
```

## Security Checklist

- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall (UFW)
- [ ] Set up fail2ban
- [ ] Enable database encryption
- [ ] Regular security updates
- [ ] Configure CORS properly
- [ ] Set up monitoring and alerting
- [ ] Implement rate limiting
- [ ] Regular backups
- [ ] Audit logs

## Troubleshooting

### Database Connection Issues

```bash
# Check database logs
docker-compose logs postgres

# Test connection
docker-compose exec backend python -c "from app.core.database import engine; print(engine.connect())"
```

### Frontend Not Loading

```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Scale services
docker-compose up -d --scale backend=3
```

## Cloud Deployment

### AWS

Use AWS ECS or EKS for container orchestration.

### Google Cloud

Deploy to Google Cloud Run or GKE.

### DigitalOcean

Use DigitalOcean App Platform or Droplets with Docker.

## Support

For deployment issues:
- Check logs: `docker-compose logs -f`
- Review configuration files
- Check GitHub issues
- Contact support team
