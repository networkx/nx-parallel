# Release process for `nx-parallel`

## Introduction

Example `version number`

- 1.8.dev0 # development version of 1.8 (release candidate 1)
- 1.8rc1 # 1.8 release candidate 1
- 1.8rc2.dev0 # development version of 1.8 release candidate 2
- 1.8 # 1.8 release
- 1.9.dev0 # development version of 1.9 (release candidate 1)

## Process

- Set release variables:

      export VERSION=<version number>
      export PREVIOUS=<previous version number>
      export ORG="networkx"
      export REPO="nx-parallel"

- Autogenerate release notes

      changelist ${ORG}/${REPO} v${PREVIOUS} main --version ${VERSION}

- Put the output of the above command at the top of `CHANGELOG.md`

- Update `__version__` in `nx_parallel/__init__.py`.

- Commit changes:

      git add nx_parallel/__init__.py CHANGELOG.md
      git commit -m "Designate ${VERSION} release"

- Tag the release in git:

      git tag -s v${VERSION} -m "signed ${VERSION} tag"

  If you do not have a gpg key, use -u instead; it is important for
  Debian packaging that the tags are annotated

- Push the new meta-data to github:

      git push --tags origin main

  where `origin` is the name of the `github.com:networkx/nx-parallel`
  repository

- Review the github release page:

      https://github.com/networkx/nx-parallel/tags

- Update `__version__` in `nx_parallel/__init__.py`.

- Commit changes:

      git add nx_parallel/__init__.py
      git commit -m 'Bump version'
      git push origin main
