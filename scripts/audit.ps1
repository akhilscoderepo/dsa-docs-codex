param(
    [Parameter(Mandatory = $true)][ValidatePattern('^\d{2}$')][string]$Chapter,
    [switch]$Draft,
    [switch]$UpdateIds
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$python = if ($env:PYTHON) { $env:PYTHON } else { 'C:\Users\Akhil\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' }
$chapterDir = Get-ChildItem -LiteralPath (Join-Path $repo 'dsa-skills\manuscripts') -Directory | Where-Object Name -Like "$Chapter-*" | Select-Object -First 1
$spec = Get-ChildItem -LiteralPath (Join-Path $repo 'dsa-skills\chapter-specs') -File | Where-Object Name -Like "$Chapter-*.md" | Select-Object -First 1
if (-not $chapterDir -or -not $spec) { throw "Could not resolve chapter or specification for $Chapter" }

$auditor = Join-Path $repo 'dsa-skills\dsa-curriculum-auditor\scripts\audit_manuscripts.py'
$stamp = Join-Path $repo "dsa-skills\validation\$($chapterDir.BaseName).json"
$scratch = Join-Path $repo 'tmp\java-validation'
$env:PYTHONPATH = @((Join-Path $repo 'tmp\html-deps'), $env:PYTHONPATH) -join [IO.Path]::PathSeparator
$args = @($auditor, $chapterDir.FullName, '--spec', $spec.FullName, '--release', '25', '--workdir', $scratch, '--stamp', $stamp)
if ($Draft) { $args += '--draft' }
if ($UpdateIds) { $args += '--update-ids' }
& $python @args
exit $LASTEXITCODE

