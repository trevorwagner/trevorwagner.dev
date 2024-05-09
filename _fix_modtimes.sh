#!/usr/bin/env sh
if [ $# = 0 ]; then
  git ls-files -z |xargs -0 sh "$0"
  exit $?
fi

for file in "$@"; do
  time="$(git log --pretty=format:%cd -n 1 \
                  --date=format:%Y%m%d%H%M.%S --date-order -- "$file")"
  if [ -z "$time" ]; then
    echo "ERROR: skipping '$file' -- no git log found" >&2
    continue
  fi
  touch -m -t "$time" "$file"
done

