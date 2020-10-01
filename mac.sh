#!/bin/sh

if printf '%s' "$0" | grep '/' -; then
	script_dir="$( printf '%s' "$0" | rev | cut -d'/' -f2- | rev)"
else
	script_dir="$PWD"
fi

# If not in working directory of script, chdir into it
if [ "$PWD" != "$script_dir" ]; then
	cd "$script_dir" || printf 'Directory %s does not exist!' "$script_dir"; exit 1
fi 

. .venv/bin/activate
python3 app.py
