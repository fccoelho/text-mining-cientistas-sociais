#!/usr/bin/env bash
jb build -W -n --keep-going .
ghp-import -n -p -f _build/html


