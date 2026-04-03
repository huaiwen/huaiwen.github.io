# Deployment Notes

This repository is deployed as a Jekyll-style static site:

- GitHub stores the source and runs the build in GitHub Actions.
- The server `14.103.72.107` is the only production entry point.
- Nginx serves `/var/www/huaiwen.me/current` directly.
- GitHub Pages is no longer the production host.

Files in this directory:

- `init-server.sh`: initialize an Ubuntu 22.04 server.
- `nginx-http-bootstrap.conf`: temporary HTTP config used before issuing the TLS certificate.
- `nginx-huaiwen.me.conf`: final HTTPS config for production.

Legacy files to retire after the new pipeline is verified:

- `.travis.yml`: old Travis CI pipeline that built Jekyll and deployed to `gh-pages`
- `CNAME`: GitHub Pages custom-domain file; not needed once production no longer depends on GitHub Pages

Security note:

- `.travis.yml` currently contains a hard-coded GitHub token from the old deployment flow.
- After the GitHub Actions pipeline is confirmed working, remove `.travis.yml` and revoke that old token if it is still active.
