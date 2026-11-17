#!/bin/sh
# Remove Python bytecode caches under the project root.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
removed=0

remove_listed() {
  list=$1
  if [ -z "$list" ]; then
    return
  fi
  printf '%s\n' "$list" | while IFS= read -r path; do
    rm -rf "$path"
    printf 'removed %s\n' "${path#"$ROOT"/}"
  done
  count=$(printf '%s\n' "$list" | wc -l | tr -d ' ')
  removed=$((removed + count))
}

dirs=$(find "$ROOT" -type d -name '__pycache__')
remove_listed "$dirs"

files=$(find "$ROOT" -type f \( -name '*.pyc' -o -name '*.pyo' \))
remove_listed "$files"

if [ "$removed" -eq 0 ]; then
  echo "no pycache found"
else
  echo "done, removed $removed item(s)"
fi
