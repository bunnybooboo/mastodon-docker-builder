# mastodon-docker-builder

A Mastodon image builder, generating images optimized for stateless containers and quick deployments.

Compared to gargron/mastodon:

- Code isn't writable for the `mastodon` user (nothing is except `/mastodon/tmp/`)
- Assets are generated in the Dockerfile and stored in the image, removing the need to have two volumes for it and the very slow chown, making rolling upgrades smoother.

On Docker Hub: https://hub.docker.com/r/maastodon/mastodon-docker/

Included themes:

- <https://github.com/skiant/mastodon-light-theme>
- <https://github.com/Sylvhem/witches-town-theme>

Image versions:

- 0.3: Added witches\_town theme
- 0.2: Added mastodon\_light theme
- 0.1: Initial version

