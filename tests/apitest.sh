#!/usr/bin/env bash
# blackman-mirrors is a fork of Manjaro pacman-mirrors
BRANCH=$( (pacman-mirrors --api --get-branch >&1) 2>&1 )
echo "branch is '${BRANCH}'"
