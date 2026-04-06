param(
    [string]$Payload = "",
    [string]$Policy = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
$PythonFile = Join-Path $RepoRoot "server\finops_guard_lite_local.py"

function Resolve-RepoPath {
    param(
        [string]$BaseRoot,
        [string]$InputPath
    )

    if ([string]::IsNullOrWhiteSpace($InputPath)) {
        return ""
    }

    if ([System.IO.Path]::IsPathRooted($InputPath)) {
        return [System.IO.Path]::GetFullPath($InputPath)
    }

    return [System.IO.Path]::GetFullPath((Join-Path $BaseRoot $InputPath))
}

if ([string]::IsNullOrWhiteSpace($Payload)) {
    $Payload = "examples\example_local_allow.json"
}
if ([string]::IsNullOrWhiteSpace($Policy)) {
    $Policy = "policies\finops_local_policy_v1.json"
}

$Payload = Resolve-RepoPath -BaseRoot $RepoRoot -InputPath $Payload
$Policy  = Resolve-RepoPath -BaseRoot $RepoRoot -InputPath $Policy

if (!(Test-Path -LiteralPath $PythonFile)) { throw "Missing: $PythonFile" }
if (!(Test-Path -LiteralPath $Payload))    { throw "Missing payload: $Payload" }
if (!(Test-Path -LiteralPath $Policy))     { throw "Missing policy: $Policy" }

python $PythonFile $Payload $Policy