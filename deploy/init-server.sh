#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   sudo bash deploy/init-server.sh [deploy_user]
#
# Example:
#   sudo bash deploy/init-server.sh deploy

DEPLOY_USER="${1:-deploy}"
SITE_ROOT="/var/www/huaiwen.me"

apt update
apt install -y nginx rsync certbot python3-certbot-nginx ufw

if ! id -u "${DEPLOY_USER}" >/dev/null 2>&1; then
  adduser --disabled-password --gecos "" "${DEPLOY_USER}"
fi

usermod -aG www-data "${DEPLOY_USER}"

mkdir -p "${SITE_ROOT}/acme"
mkdir -p "${SITE_ROOT}/releases/initial"

cat > "${SITE_ROOT}/releases/initial/index.html" <<'EOF'
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>huaiwen.me</title>
</head>
<body>
  <h1>huaiwen.me</h1>
  <p>Server initialized. Waiting for first deployment.</p>
</body>
</html>
EOF

ln -sfn "${SITE_ROOT}/releases/initial" "${SITE_ROOT}/current"

chown -R "${DEPLOY_USER}:www-data" "${SITE_ROOT}"
find "${SITE_ROOT}" -type d -exec chmod 775 {} \;
find "${SITE_ROOT}" -type f -exec chmod 664 {} \;

mkdir -p "/home/${DEPLOY_USER}/.ssh"
touch "/home/${DEPLOY_USER}/.ssh/authorized_keys"
chmod 700 "/home/${DEPLOY_USER}/.ssh"
chmod 600 "/home/${DEPLOY_USER}/.ssh/authorized_keys"
chown -R "${DEPLOY_USER}:${DEPLOY_USER}" "/home/${DEPLOY_USER}/.ssh"

ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

echo
echo "Server initialized."
echo "Next steps:"
echo "1. Append the GitHub Actions public key to /home/${DEPLOY_USER}/.ssh/authorized_keys"
echo "2. Install the Nginx site config from deploy/nginx-http-bootstrap.conf"
echo "3. Issue the Let's Encrypt certificate"
echo "4. Switch to deploy/nginx-huaiwen.me.conf"
