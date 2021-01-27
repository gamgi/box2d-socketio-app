#!/bin/bash
set -euo pipefail

FILE_PATTERN='*_interfaces.py'
OUTPUT_DIR="../frontend/src/lib/generated/"
BUILD_COMMAND="pipenv run py-ts-interfaces"

echo "compiling files matching '${FILE_PATTERN}'"

# compile files
SUFFIX="${FILE_PATTERN#'*'}"
find ./ -type f -name "$FILE_PATTERN" -exec \
    bash -c "$BUILD_COMMAND \${0} -o $OUTPUT_DIR\${0/%${SUFFIX}/Interfaces.ts}" {} \;

# rewrite them to export, capitalize, fix bugs and pass lint 
find "$OUTPUT_DIR" -type f -name '*.ts' -exec \
    sed -i \
    -e "s/^interface/export interface/" \
    -e "s/^    /  /" \
    -e "s/^  vertices: Array<\[number\]>;$/  vertices: Array<\[number, number\]>;/" \
    -e "1 i /* eslint-disable @typescript-eslint/array-type */" \
    -e "1 i /* eslint-disable camelcase */" {} \;

echo "done";