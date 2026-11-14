# Tools installation

## TL;DR

- You need **Git**, **uv** (which installs Python), **Node.js 24** with **pnpm**, **Docker** and the **GitHub CLI** (`gh`). pre-commit runs through uv.
- On **Windows**, install **WSL 2** first and do everything inside Ubuntu.
- Everything here is free.
- Total time: about 30 minutes on a good connection.
- At the end, run the [check commands](#7-check-everything) to confirm the setup.

## Versions

| Tool | Minimum version | Why |
|---|---|---|
| Git | 2.40 | Version control |
| uv | 0.13.8 | Python versions, environments, dependencies ([docs](https://docs.astral.sh/uv/)) |
| Python | 3.12 | Installed by uv, nothing to do |
| Node.js | 24 LTS | Front-end projects |
| pnpm | the version in each project's `packageManager` field | Front-end dependencies |
| Docker | Docker Engine or Docker Desktop with Compose v2 | Run services (database, Redis) and projects |
| GitHub CLI | 2.x | Pull requests, issues, checkout of PRs from the terminal |

## 1. Windows only: install WSL 2

Open **PowerShell as administrator**:

```powershell
wsl --install -d Ubuntu
```

Restart the computer, open **Ubuntu** from the Start menu, and create a Linux user. From now on, run every command of this guide **inside Ubuntu**, and keep your code in the Linux file system (for example `~/code`), not in `/mnt/c/...`.

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) on Windows and enable **Settings → Resources → WSL integration** for Ubuntu. Docker Desktop is free for personal use, education, non-commercial open source projects and small businesses; check its license terms for your situation.

## 2. Install Git and the basic tools

**Ubuntu / Debian / WSL:**

```bash
sudo apt update
sudo apt install -y git curl build-essential
```

**macOS** (with [Homebrew](https://brew.sh/)):

```bash
xcode-select --install      # Apple command line tools, includes Git
brew install git
```

## 3. Install uv (and Python)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# open a new terminal, then:
uv --version
uv python install 3.12
```

Update uv later with `uv self update`. You do not install pre-commit, Ruff or mypy globally: projects run them with `uv run` and `uvx`.

## 4. Configure Git

```bash
git config --global user.name "Your Name"
git config --global user.email "your-github-noreply-address@users.noreply.github.com"
git config --global init.defaultBranch main
git config --global pull.ff only
git config --global fetch.prune true
```

To keep your e-mail address private, use the **noreply** address shown in GitHub **Settings → Emails** ("Keep my email addresses private").

**Connect to GitHub with SSH** (recommended):

```bash
ssh-keygen -t ed25519 -C "your-github-noreply-address@users.noreply.github.com"
cat ~/.ssh/id_ed25519.pub     # copy the output
```

Add the key in GitHub **Settings → SSH and GPG keys → New SSH key** as an **Authentication key**.

**Sign your commits with the same key** (recommended, rule COM-010):

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

Add the same public key again in GitHub, this time as a **Signing key**. Your commits then show a "Verified" badge.

**Enable two-factor authentication** on your GitHub account (Settings → Password and authentication). DAH Labs requires it (rule GH-008).

## 5. Install Node.js 24 and pnpm

Use [nvm](https://github.com/nvm-sh/nvm) to manage Node.js versions:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.41.0/install.sh | bash
# open a new terminal, then:
nvm install 24
nvm alias default 24
corepack enable              # makes pnpm available, at the version each project asks for
pnpm --version
```

The command installs nvm `v0.41.0`, the latest release on 2026-11-13. Check the [nvm README](https://github.com/nvm-sh/nvm#installing-and-updating) for newer versions.

Node.js 25 and newer do not include corepack. If you use them anyway, install corepack with `npm install --global corepack`, or use the [pnpm standalone installer](https://pnpm.io/installation). In a project folder that has a `.nvmrc` file, `nvm use` selects the right version.

## 6. Install Docker and the GitHub CLI

**Ubuntu / Debian** (not WSL with Docker Desktop): follow the official [Docker Engine installation guide](https://docs.docker.com/engine/install/ubuntu/), then allow your user to run Docker:

```bash
sudo usermod -aG docker "$USER"     # log out and in again
```

**macOS:** install [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Colima](https://github.com/abiosoft/colima) (`brew install colima docker docker-compose`).

**GitHub CLI:**

```bash
# Ubuntu / Debian / WSL: follow https://github.com/cli/cli/blob/trunk/docs/install_linux.md
# macOS:
brew install gh
# then, everywhere:
gh auth login
```

## 7. Check everything

```bash
git --version          # 2.40 or newer
uv --version           # 0.13.8 or newer
uv run --python 3.12 python --version
node --version         # v24.x
pnpm --version
docker run --rm hello-world
docker compose version
gh auth status
```

If one command fails, see [Troubleshooting](#troubleshooting), then ask in the repository with the **Question** issue form.

## Troubleshooting

| Problem | Solution |
|---|---|
| `uv: command not found` after install | Open a new terminal, or run `source ~/.bashrc` (`~/.zshrc` on macOS). |
| `nvm: command not found` | Same as above. |
| `permission denied` on the Docker socket | `sudo usermod -aG docker "$USER"`, then log out and in again. |
| Very slow `git` or `uv` in WSL | Your code is in `/mnt/c/…`: move it to `~/code`. |
| `corepack: command not found` | You use Node.js 25 or newer: `npm install --global corepack`. |
| Slow downloads | uv and pnpm cache everything: the second install is fast. Prefer a stable connection for the first one. |

## Checklist

- [ ] (Windows) WSL 2 with Ubuntu is installed and the code lives in `~/code`.
- [ ] Git is configured with a name and a (noreply) e-mail address.
- [ ] An SSH key is added to GitHub; commit signing is configured (recommended).
- [ ] Two-factor authentication is enabled on GitHub.
- [ ] uv, Python 3.12, Node.js 24, pnpm, Docker and `gh` pass the check commands.

---

*Last verified: 2026-11-13.*
