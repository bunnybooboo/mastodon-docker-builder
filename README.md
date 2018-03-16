# mastodon-docker-builder

A Mastodon image builder, generating images optimized for stateless containers and quick deployments.

Compared to gargron/mastodon:

- Code isn't writable for the `mastodon` user (nothing is except `/mastodon/tmp/`)
- Assets are generated in the Dockerfile and stored in the image, removing the need to have two volumes for it and the very slow chown, making rolling upgrades smoother.

On Docker Hub: https://hub.docker.com/r/maastodon/mastodon-docker/
