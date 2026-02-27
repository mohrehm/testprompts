param(
    [Parameter(Mandatory = $false)]
    [ValidateSet("quick", "deep")]
    [string]$Mode = "deep",

    [Parameter(Mandatory = $false)]
    [string]$Topic = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Step([string]$Message) {
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Assert-FileExists([string]$Path, [string]$Hint) {
    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Missing required file: $Path`nHint: $Hint"
    }
}

function Pause-ForOperator([string]$Instruction) {
    Write-Host ""
    Write-Host $Instruction -ForegroundColor Yellow
    Read-Host "Press Enter after you complete this step in Copilot Chat"
}

Step "Pipeline bootstrap"
Write-Host "Mode : $Mode"
if ($Topic) { Write-Host "Topic: $Topic" }

Assert-FileExists "docs/orchestration/pipeline.md" "Create orchestration contract first."
Assert-FileExists "docs/prompts/researcher-mslearn.md" "Add specialist prompt pack."
Assert-FileExists "docs/prompts/validator-gotchas.md" "Add specialist prompt pack."
Assert-FileExists "docs/prompts/security-reviewer.md" "Add specialist prompt pack."

Step "Stage 1 - Research"
Pause-ForOperator "Open docs/prompts/researcher-mslearn.md, paste prompt into Copilot Chat, and generate/update artifacts/research/research.md."
Assert-FileExists "artifacts/research/research.md" "Run stage 1 and save research artifact."
python .github/scripts/validate_research.py --stage research

Step "Stage 2 - Validate/Gotchas"
Pause-ForOperator "Open docs/prompts/validator-gotchas.md, paste prompt into Copilot Chat, and refine artifacts/research/research.md."
python .github/scripts/validate_research.py --stage research

Step "Stage 3 - Security (required)"
Pause-ForOperator "Open docs/prompts/security-reviewer.md, paste prompt into Copilot Chat, and create/update artifacts/security/securityassessment.md."
Assert-FileExists "artifacts/security/securityassessment.md" "Security stage is mandatory."
python .github/scripts/validate_research.py --stage security

Step "Stage 4 - Full validation"
python .github/scripts/validate_research.py --stage full

Write-Host ""
Write-Host "Orchestration complete. Artifacts are ready for PR." -ForegroundColor Green

