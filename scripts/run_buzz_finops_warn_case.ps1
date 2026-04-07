param(
    [string]$Payload = "",
    [string]$Output = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Runner = Join-Path $RepoRoot "scripts\run_buzz_finops_live_adapter.ps1"

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
    $Payload = "runtime\imports\buzz_edge_warn_payload_v1.json"
}
if ([string]::IsNullOrWhiteSpace($Output)) {
    $Output = "runtime\imports\buzz_edge_warn_result_v1.json"
}

$Payload = Resolve-RepoPath -BaseRoot $RepoRoot -InputPath $Payload
$Output  = Resolve-RepoPath -BaseRoot $RepoRoot -InputPath $Output

if (!(Test-Path -LiteralPath $Runner)) { throw "Missing runner: $Runner" }
if (!(Test-Path -LiteralPath $Payload)) { throw "Missing payload: $Payload" }

powershell -ExecutionPolicy Bypass -File $Runner -Payload $Payload -Output $Output