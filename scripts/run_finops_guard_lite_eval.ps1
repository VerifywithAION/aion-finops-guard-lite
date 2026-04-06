param(
    [string]$Payload = "",
    [string]$Policy = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
$PythonFile = Join-Path $RepoRoot "server\finops_guard_lite.py"

if ([string]::IsNullOrWhiteSpace($Payload)) {
    $Payload = Join-Path $RepoRoot "examples\example_allow.json"
}
if ([string]::IsNullOrWhiteSpace($Policy)) {
    $Policy = Join-Path $RepoRoot "policies\finops_policy_v1.json"
}

if (!(Test-Path -LiteralPath $PythonFile)) { throw "Missing: $PythonFile" }
if (!(Test-Path -LiteralPath $Payload)) { throw "Missing payload: $Payload" }
if (!(Test-Path -LiteralPath $Policy)) { throw "Missing policy: $Policy" }

python $PythonFile $Payload $Policy