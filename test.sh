#!/bin/zsh

input='{"files":[{"path":".darglint","additions":2,"deletions":0},{"path":".github/workflows/pr-linting.yaml","additions":7,"deletions":3},{"path":"README.md","additions":26,"deletions":0},{"path":"bin/get_config.py","additions":77,"deletions":25},{"path":"pytmac.py","additions":78,"deletions":38}]}'

if [[ $(echo $input | jq -r '.files[] | select(.path | contains(".py")) | .path') > 0 ]]; then
    echo "python_changed=true" >> "$GITHUB_OUTPUT"
else
    echo "python_changed=false" >> "$GITHUB_OUTPUT"
fi
