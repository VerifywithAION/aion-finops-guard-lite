$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ApiFile = Join-Path $RepoRoot "server\finops_guard_lite_api.py"

if (!(Test-Path -LiteralPath $ApiFile)) {
    throw "Missing: $ApiFile"
}

python $ApiFile