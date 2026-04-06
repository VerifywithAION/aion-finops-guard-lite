param(
    [string]$BuzzPayload = "",
    [string]$NormalizedOut = "",
    [string]$Policy = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
$NormalizePy = Join-Path $RepoRoot "server\buzz_to_finops_import.py"
$EvalPy = Join-Path $RepoRoot "server\finops_guard_lite_import_eval.py"

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

if ([string]::IsNullOrWhiteSpace($BuzzPayload)) {
    $BuzzPayload = "runtime\imports\buzz_sample_payload_v1.json"
}
if ([string]::IsNullOrWhiteSpace($NormalizedOut)) {
    $NormalizedOut = "runtime\imports\buzz_normalized_snapshot_v1.json"
}
if ([string]::IsNullOrWhiteSpace($Policy)) {
    $Policy = "policies\finops_import_policy_v1.json"
}

$BuzzPayload   = Resolve-RepoPath -BaseRoot $RepoRoot -InputPath $BuzzPayload
$NormalizedOut = Resolve-RepoPath -BaseRoot $RepoRoot -InputPath $NormalizedOut
$Policy        = Resolve-RepoPath -BaseRoot $RepoRoot -InputPath $Policy

if (!(Test-Path -LiteralPath $NormalizePy)) { throw "Missing: $NormalizePy" }
if (!(Test-Path -LiteralPath $EvalPy))      { throw "Missing: $EvalPy" }
if (!(Test-Path -LiteralPath $BuzzPayload)) { throw "Missing Buzz payload: $BuzzPayload" }
if (!(Test-Path -LiteralPath $Policy))      { throw "Missing policy: $Policy" }

python $NormalizePy $BuzzPayload $NormalizedOut
python $EvalPy $NormalizedOut $Policy