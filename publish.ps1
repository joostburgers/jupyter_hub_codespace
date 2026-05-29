# =============================================================================
# publish.ps1 - Project: Mapping Emotions  (Windows / VS Code workaround)
# =============================================================================
# Equivalent to publish.sh for Windows users who cannot run bash directly.
#
# Run from the repo root in a PowerShell terminal:
#   .\publish.ps1
#
# GitHub Pages must be enabled for this repo with source set to:
#   Branch: main  |  Folder: /docs
# =============================================================================

$ErrorActionPreference = 'Stop'

$RepoRoot   = $PSScriptRoot
$ProjectDir = Join-Path $RepoRoot 'project_mapping_emotions'
$Docs       = Join-Path $RepoRoot 'docs'

Write-Host ""
Write-Host "=============================================="
Write-Host " Project: Mapping Emotions - Publish Script"
Write-Host "=============================================="
Write-Host ""

# -----------------------------------------------------------------------------
# STEP 1: Regenerate team_data.json from lesson_1_the_team/data/team.csv
# -----------------------------------------------------------------------------
Write-Host "Step 1/5: Regenerating team data from team.csv..."

$TeamScript = Join-Path $RepoRoot 'lesson_1_the_team\generate_team_json.py'
try {
    python $TeamScript 2>$null
    Write-Host "          v team_data.json updated"
} catch {
    Write-Host "          ! Could not regenerate team data (team.csv may not be filled in yet)"
    Write-Host "            Using existing team_data.json if present"
}

# -----------------------------------------------------------------------------
# STEP 2: Convert whitepaper notebook to HTML
# -----------------------------------------------------------------------------
Write-Host "Step 2/5: Exporting whitepaper notebook to HTML..."

$Notebook = Join-Path $ProjectDir 'project_part_2_whitepaper.ipynb'
if (Test-Path $Notebook) {
    $nbArgs = @(
        '-m', 'jupyter', 'nbconvert',
        '--to', 'html',
        '--no-input',
        '--TagRemovePreprocessor.enabled=True',
        '--TagRemovePreprocessor.remove_cell_tags=["remove_cell"]',
        '--TagRemovePreprocessor.remove_all_outputs_tags=["remove_output"]',
        '--output', 'whitepaper.html',
        '--output-dir', $ProjectDir,
        $Notebook
    )
    try {
        python @nbArgs
        Write-Host "          v whitepaper.html generated"
    } catch {
        Write-Host "          ! nbconvert failed - using existing whitepaper.html"
    }
} else {
    Write-Host "          ! Notebook not found - using existing whitepaper.html"
}

# Inject site navigation via the shared Python script
$Whitepaper  = Join-Path $ProjectDir 'whitepaper.html'
$WrapScript  = Join-Path $RepoRoot 'wrap_whitepaper.py'
if ((Test-Path $Whitepaper) -and (Test-Path $WrapScript)) {
    python $WrapScript $Whitepaper
    Write-Host "          v whitepaper.html wrapped with site navigation"
}

# -----------------------------------------------------------------------------
# STEP 3: Assemble docs/ folder (GitHub Pages target)
# -----------------------------------------------------------------------------
Write-Host "Step 3/5: Assembling docs/ folder..."

New-Item -ItemType Directory -Force -Path $Docs       | Out-Null
New-Item -ItemType Directory -Force -Path "$Docs\images" | Out-Null

# Core website pages
Copy-Item (Join-Path $ProjectDir 'index.html')                    (Join-Path $Docs 'index.html')            -Force
Copy-Item (Join-Path $ProjectDir 'team.html')                     (Join-Path $Docs 'team.html')             -Force
Copy-Item (Join-Path $ProjectDir 'interactive_tour.html')         (Join-Path $Docs 'interactive_tour.html') -Force
Copy-Item (Join-Path $ProjectDir 'whitepaper.html')               (Join-Path $Docs 'whitepaper.html')       -Force
Copy-Item (Join-Path $ProjectDir 'styles.css')                    (Join-Path $Docs 'styles.css')            -Force
Copy-Item (Join-Path $ProjectDir 'interactive_tour_config.js')    (Join-Path $Docs 'interactive_tour_config.js') -Force

# Team data
$TeamJson = Join-Path $ProjectDir 'team_data.json'
if (Test-Path $TeamJson) {
    Copy-Item $TeamJson (Join-Path $Docs 'team_data.json') -Force
    Write-Host "          v team_data.json included"
} else {
    Write-Host "          ! team_data.json not found - team page will show no members"
}

# Images (headshots, etc.)
$ImgSrc = Join-Path $ProjectDir 'images'
if (Test-Path $ImgSrc) {
    Copy-Item "$ImgSrc\*" (Join-Path $Docs 'images') -Recurse -Force
    Write-Host "          v images copied"
}

# Prevent GitHub Pages from running Jekyll processing
New-Item -ItemType File -Force -Path (Join-Path $Docs '.nojekyll') | Out-Null

Write-Host "          v docs/ assembled"

# -----------------------------------------------------------------------------
# STEP 4: Commit
# -----------------------------------------------------------------------------
Write-Host "Step 4/5: Committing changes..."

Set-Location $RepoRoot
git add docs/ project_mapping_emotions/whitepaper.html project_mapping_emotions/team_data.json lesson_1_the_team/data/team.csv 2>$null

$diff = git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "          i No new changes to commit - site is already up to date"
} else {
    $Student = git config user.name 2>$null
    if (-not $Student) { $Student = "Unknown" }
    $Timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm'
    git commit -m "Publish site - $Student - $Timestamp"
    Write-Host "          v committed"
}

# -----------------------------------------------------------------------------
# STEP 5: Push
# -----------------------------------------------------------------------------
Write-Host "Step 5/5: Pushing to GitHub..."
git push
Write-Host "          v pushed"

# Derive the live GitHub Pages URL from the git remote
$Remote = git remote get-url origin 2>$null
if ($Remote -match 'https://github\.com/([^/]+)/([^/.]+)') {
    $GithubUser = $Matches[1]; $RepoName = $Matches[2]
} elseif ($Remote -match 'git@github\.com:([^/]+)/([^/.]+)') {
    $GithubUser = $Matches[1]; $RepoName = $Matches[2]
} else {
    $GithubUser = 'your-username'; $RepoName = 'your-repo'
}

Write-Host ""
Write-Host "=============================================="
Write-Host " Done!"
Write-Host " Your site will be live in ~1 minute at:"
Write-Host " https://$GithubUser.github.io/$RepoName/"
Write-Host ""
Write-Host " Pages:"
Write-Host "   Home          -> https://$GithubUser.github.io/$RepoName/"
Write-Host "   Team          -> https://$GithubUser.github.io/$RepoName/team.html"
Write-Host "   Interactive   -> https://$GithubUser.github.io/$RepoName/interactive_tour.html"
Write-Host "   Whitepaper    -> https://$GithubUser.github.io/$RepoName/whitepaper.html"
Write-Host "=============================================="
Write-Host ""
