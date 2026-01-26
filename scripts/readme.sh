#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
DEMO_DB="$SCRIPT_DIR/demo_db.sh"
TEMPLATE="$SCRIPT_DIR/README_TEMPLATE.md"
PLACEHOLDER="{{PLACEHOLDER}}"
COMMANDS="$SCRIPT_DIR/README_COMMANDS.txt"
TMP="$(mktemp)"
DISCLAIMER="<!-- This README is generated and should not be edited directly. Instead edit the template at scripts/README_TEMPLATE.md -->"
OUT="$SCRIPT_DIR/../README.md"

to_value ()
{
local cmd="$1"
local result="$(eval "$cmd")"
local status=$?
(( status == 0 )) || exit "$status"

local block=$(
cat <<EOF
\`\`\`sh
\$ $cmd
$result
\`\`\`
EOF
)

printf '%s' "$block"
}

export CONSUMPTION_CONFIG_DIR=.
export CONSUMPTION_DATA_DIR=.
export CONSUMPTION_LOG_DIR=.
echo "> DEMO DB GENERATION START <"
eval "$DEMO_DB"
echo "> DEMO DB GENERATION END <"

echo "Temporary README Location: $TMP"
cp "$TEMPLATE" "$TMP"

while IFS= read -r cmd; do
    block="$(to_value "$cmd")"
    awk -v block="$block" "!done && sub(/$PLACEHOLDER/, block) { done = 1 } { print }" "$TMP" > "$TMP.tmp"
    mv "$TMP.tmp" "$TMP"
done < "$COMMANDS"

{ printf '%s\n' "$DISCLAIMER"; cat "$TMP"; } > "$TMP.tmp"

mv "$TMP.tmp" "$OUT"
