#!/usr/bin/env bash
jb build -W -n --keep-going Book/
cp -R Book/_build/html/* _build/html/
ghp-import -n -p -f Book/_build/html


