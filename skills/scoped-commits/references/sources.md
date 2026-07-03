# Scoped Commits — References

## Origin article

- **Sumner Evans** — *Stop Using Conventional Commits*
  https://sumnerevans.com/posts/software-engineering/stop-using-conventional-commits/

  The article that named the pattern and systematically debunks Conventional Commits' selling points (automated changelogs, semver bumping, communication, build automation, contributor experience). Evans coined the "Scoped Commits" label and created scopedcommits.com as a counterweight to Conventional Commits' industry dominance.

## Scoped Commits standard

- https://scopedcommits.com

## Projects using this format in the wild

These projects use the `scope: description` format organically, without calling it "Scoped Commits":

| Project | Commit log |
|---|---|
| Linux kernel | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/ |
| Git | https://github.com/git/git/commits/master |
| Go | https://github.com/golang/go/commits/master |
| FreeBSD | https://cgit.freebsd.org/src/log/ |
| NixOS/nixpkgs | https://github.com/NixOS/nixpkgs/commits/master |

## Real examples from those projects

```
# Linux kernel
i2c: virtio: mark device ready before registering the adapter

# Go
net/http/cookiejar: add godoc links

# Git
gitlab-ci: update macOS image
```
