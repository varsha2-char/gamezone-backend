# 🎮 GameZone — Snake Game (React + FastAPI)

## Project Structure
```
gamezone/
├── backend/
│   ├── main.py           # FastAPI backend
│   └── requirements.txt  # Python dependencies
└── frontend/
    └── index.html        # Game frontend (single file)
```

---

## 🚀 AWS Deployment Guide (Step by Step)

---

### STEP 1 — Launch an EC2 Instance (Backend)

1. Go to **AWS Console → EC2 → Launch Instance**
2. Choose:
   - AMI: **Ubuntu 22.04 LTS**
   - Instance type: **t2.micro** (free tier eligible)
3. Create or select a **Key Pair** (download the `.pem` file)
4. Under **Security Group**, open these ports:
   - SSH: port 22
   - HTTP: port 80
   - Custom TCP: port 8000 (for FastAPI)
5. Click **Launch**

---

### STEP 2 — Connect to EC2 & Set Up Backend

```bash
# Connect via SSH (replace with your key and IP)
ssh -i "your-key.pem" ubuntu@YOUR_EC2_PUBLIC_IP

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3-pip python3-venv -y

# Create project directory
mkdir gamezone && cd gamezone

# Upload backend files (run this from your LOCAL machine)
# scp -i your-key.pem backend/main.py ubuntu@YOUR_IP:~/gamezone/
# scp -i your-key.pem backend/requirements.txt ubuntu@YOUR_IP:~/gamezone/

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test the server
uvicorn main:app --host 0.0.0.0 --port 8000
# Visit: http://YOUR_EC2_IP:8000 → should see {"message":"GameZone API is running!"}
```

---

### STEP 3 — Run Backend as a Service (PM2 / systemd)

```bash
# Create systemd service so it runs forever
sudo nano /etc/systemd/system/gamezone.service
```

Paste this content:
```ini
[Unit]
Description=GameZone FastAPI
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/gamezone
ExecStart=/home/ubuntu/gamezone/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable gamezone
sudo systemctl start gamezone
sudo systemctl status gamezone   # Should show: active (running)
```

---

### STEP 4 — Deploy Frontend to AWS S3

1. Go to **AWS Console → S3 → Create Bucket**
   - Bucket name: `gamezone-frontend` (must be unique)
   - Region: same as EC2
   - **Uncheck** "Block all public access"

2. Upload `frontend/index.html` to the bucket

3. Enable **Static Website Hosting**:
   - Go to bucket → **Properties** → **Static website hosting** → Enable
   - Index document: `index.html`

4. Set **Bucket Policy** (Permissions tab):
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::gamezone-frontend/*"
  }]
}
```

5. Your frontend URL will be:
   `http://gamezone-frontend.s3-website-REGION.amazonaws.com`

---

### STEP 5 — Connect Frontend to Backend

Edit `frontend/index.html` line:
```javascript
const API = "http://YOUR_EC2_PUBLIC_IP:8000";
```
Replace `YOUR_EC2_PUBLIC_IP` with your actual EC2 IP, then re-upload to S3.

---

### STEP 6 (Optional) — Add Domain + HTTPS

1. **Route 53** → Register or transfer a domain
2. **CloudFront** → Create distribution pointing to your S3 bucket
3. **AWS Certificate Manager** → Request a free SSL certificate
4. Attach the certificate to your CloudFront distribution

---

### STEP 7 (Optional) — Use RDS Instead of JSON File

```bash
# Install postgres driver
pip install asyncpg databases sqlalchemy

# Update main.py to use RDS connection string:
# DATABASE_URL = "postgresql://user:pass@YOUR_RDS_ENDPOINT/gamezone"
```

---

## ✅ Quick Test Checklist

- [ ] EC2 instance running
- [ ] `http://YOUR_IP:8000` returns JSON
- [ ] `http://YOUR_IP:8000/leaderboard` returns `[]`
- [ ] Frontend loads in browser
- [ ] Game plays and score saves
- [ ] Leaderboard shows scores

---

## 💰 AWS Free Tier Cost Estimate

| Service | Usage | Cost |
|---------|-------|------|
| EC2 t2.micro | 750 hrs/month | **FREE** |
| S3 | < 5GB | **FREE** |
| Data transfer | < 15GB | **FREE** |
| **Total** | | **$0/month** |
