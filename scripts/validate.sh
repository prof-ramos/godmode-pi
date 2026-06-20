#!/usr/bin/env bash
set -euo pipefail

DIR="${1:-.}"
FAILED=0

check() {
    local file="$1"
    local msg="$2"
    if [ -f "$DIR/$file" ]; then
        echo "$file: $msg"
    else
        echo "$file: MISSING"
        FAILED=1
    fi
}

# --- config.yml ---
if [ -f "$DIR/config.yml" ]; then
    python3 -c "
import sys, re
content = open('$DIR/config.yml').read()
assert re.search(r'^\w+:', content, re.MULTILINE), 'config.yml: no top-level key found'
assert 'systemPrompt' in content, 'config.yml: missing systemPrompt key'
print('config.yml: OK (basic structure)')
" || { echo "config.yml: INVALID"; FAILED=1; }
else
    echo "config.yml: MISSING"; FAILED=1
fi

# --- prefill.json ---
if [ -f "$DIR/prefill.json" ]; then
    python3 -c "
import json, sys
d = json.load(open('$DIR/prefill.json'))
assert isinstance(d, list), 'prefill.json: root must be an array'
for i, m in enumerate(d):
    assert 'role' in m, f'prefill.json[{i}]: missing role'
    assert m['role'] in ('user', 'assistant'), f'prefill.json[{i}]: role must be user/assistant'
    assert 'content' in m, f'prefill.json[{i}]: missing content'
    assert isinstance(m['content'], str), f'prefill.json[{i}]: content must be string'
print('prefill.json: OK')
" || { echo "prefill.json: INVALID"; FAILED=1; }
else
    echo "prefill.json: MISSING"; FAILED=1
fi

# --- Modelfile-godmode ---
if [ -f "$DIR/Modelfile-godmode" ]; then
    grep -q '^FROM' "$DIR/Modelfile-godmode" || { echo "Modelfile-godmode: missing FROM"; FAILED=1; }
    grep -q '^SYSTEM' "$DIR/Modelfile-godmode" || { echo "Modelfile-godmode: missing SYSTEM"; FAILED=1; }
    [ "$FAILED" -eq 0 ] && echo "Modelfile-godmode: OK"
else
    echo "Modelfile-godmode: MISSING"; FAILED=1
fi

# --- Markdown files ---
for f in APPEND_SYSTEM.md RULES.md; do
    if [ -s "$DIR/$f" ]; then
        echo "$f: OK"
    else
        echo "$f: empty or missing"
        FAILED=1
    fi
done

if [ "$FAILED" -eq 0 ]; then
    echo "All configs valid"
else
    echo "Some configs INVALID"
    exit 1
fi
