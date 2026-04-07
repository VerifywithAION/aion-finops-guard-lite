param(
    [string]$Payload = "",
    [string]$Output = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Adapter = Join-Path $RepoRoot "server\buzz_finops_adapter_v1.py"

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
    $Payload = "runtime\imports\buzz_real_payload_ogie_v1.json"
}
if ([string]::IsNullOrWhiteSpace($Output)) {
    $Output = "runtime\imports\buzz_finops_adapter_result_v1.json"
}

$Payload = Resolve-RepoPath -BaseRoot $RepoRoot -InputPath $Payload
$Output  = Resolve-RepoPath -BaseRoot $RepoRoot -InputPath $Output

if (!(Test-Path -LiteralPath $Adapter)) { throw "Missing adapter: $Adapter" }
if (!(Test-Path -LiteralPath $Payload)) { throw "Missing payload: $Payload" }

python $Adapter $Payload $Output