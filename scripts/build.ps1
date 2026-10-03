param(
    [Parameter(Mandatory = $true)][ValidatePattern('^\d{2}$')][string]$Chapter
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$python = if ($env:PYTHON) { $env:PYTHON } else { 'C:\Users\Akhil\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' }
$node = if ($env:NODE) { $env:NODE } else { 'C:\Users\Akhil\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' }
$chapterDir = Get-ChildItem -LiteralPath (Join-Path $repo 'dsa-skills\manuscripts') -Directory | Where-Object Name -Like "$Chapter-*" | Select-Object -First 1
if (-not $chapterDir) { throw "Could not resolve manuscript directory for $Chapter" }
$stamp = Join-Path $repo "dsa-skills\validation\$($chapterDir.BaseName).json"
$out = Join-Path $repo "output\$($chapterDir.BaseName).html"
$env:PYTHONPATH = @((Join-Path $repo 'tmp\html-deps'), $env:PYTHONPATH) -join [IO.Path]::PathSeparator

& (Join-Path $PSScriptRoot 'audit.ps1') -Chapter $Chapter -UpdateIds
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $python (Join-Path $repo 'dsa-skills\markdown-textbook-html\scripts\build_html.py') $chapterDir.FullName '-o' $out '--validation' $stamp
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $python (Join-Path $repo 'dsa-skills\dsa-curriculum-auditor\scripts\audit_html.py') $out '--manuscripts' $chapterDir.FullName '--smoke' '--stamp' $stamp
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $node (Join-Path $repo 'dsa-skills\dsa-curriculum-auditor\scripts\render_check.mjs') $out (Join-Path $repo "tmp\render-$Chapter")
exit $LASTEXITCODE

