# StartUp-Investors-Blog-Hashnode

A collection of scripts, content and tooling for the "StartUp Investors" blog hosted on Hashnode. This repository holds the source files, automation, and utilities used to create, manage, and publish posts and related assets for the blog. Most of the code is written in Python.

- Primary language: Python
- Repository: JoanneKoshy/StartUp-Investors-Blog-Hashnode

## Table of contents

- [About](#about)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Deployment / Publishing](#deployment--publishing)
- [Development / Contributing](#development--contributing)
- [License](#license)
- [Contact](#contact)

## About

This project powers the StartUp Investors blog content and automation for publishing on Hashnode. It includes content (drafts, Markdown), helper scripts for formatting / converting posts, small utilities for asset handling, and deployment automation where applicable.

## Features

- Markdown-based blog content and drafts
- Python utilities for content processing and publishing
- Automation scripts for image handling, metadata, and post conversion
- Guidelines and tooling to keep posts consistent

## Tech stack

- Python (primary)
- Small JS / CSS assets for styling (where applicable)
- Shell / PowerShell helper scripts

## Getting started

### Prerequisites

- Python 3.8+ (recommend latest stable)
- pip (or poetry/pipenv if you prefer)
- Git
- (Optional) Hashnode account and API key if using an automated publisher

### Installation

1. Clone the repository
   git clone https://github.com/JoanneKoshy/StartUp-Investors-Blog-Hashnode.git
2. Enter the project directory
   cd StartUp-Investors-Blog-Hashnode
3. Create and activate a virtual environment
   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .venv\Scripts\activate     # Windows
4. Install dependencies
   pip install -r requirements.txt
   (If the repository uses poetry/pipenv, follow those instructions instead.)

## Usage

- Draft posts in the `content/` or `posts/` directory (replace with actual path used in this repo).
- Run content checks and formatting:
  python scripts/format_post.py content/my-post.md
- Convert or export posts for Hashnode publishing:
  python scripts/export_for_hashnode.py content/my-post.md --output dist/
- (Optional) Publish via API:
  python scripts/publish_to_hashnode.py --post dist/my-post.json --api-key $HASHNODE_API_KEY

Note: Replace the example script names and paths above with the actual scripts found in the repository.

## Configuration

Environment variables (examples)

- HASHNODE_API_KEY — API key/token for automated publishing (if used)
- BLOG_AUTHOR — default author name used when publishing
- MEDIA_BUCKET — path or bucket used for storing images/assets

Create a `.env` or set variables in your environment. Example `.env`:
HASHNODE_API_KEY=your_token_here
BLOG_AUTHOR="Your Name"

## Deployment / Publishing

If this repo includes a CI/CD pipeline (GitHub Actions, etc.), check `.github/workflows/` for the publishing workflow. Typical steps:

1. Build / convert post artifacts
2. Upload images/assets to CDN or object storage
3. Call Hashnode API to publish or update the post

If you want me to add or update a GitHub Actions workflow for automated publishing, tell me what behavior you want and I can create it.

## Development / Contributing

Contributions are welcome.

- Fork the repo
- Create a feature branch: git checkout -b feature/my-change
- Make changes, add tests where applicable
- Open a pull request with a clear description of changes

Please follow the repository's code style and commit conventions. If you want a CONTRIBUTING.md I can draft one.

## Tests

If there are unit tests, run them with:
pytest

(If this repo doesn't have tests yet, consider adding basic tests for utilities.)

## License

Specify your license here (e.g., MIT). If you want, I can add a LICENSE file to this repo.

## Contact

Maintainer: Joanne Koshy (JoanneKoshy)
Project: StartUp-Investors-Blog-Hashnode
Repository: https://github.com/JoanneKoshy/StartUp-Investors-Blog-Hashnode

---

Notes:
- I kept some script and path names generic because I haven't inspected the repository files. If you want, I can:
  1) Inspect the repo to replace placeholders with exact script names and paths, and then update the README; or
  2) Add this README directly to the repository (commit).
