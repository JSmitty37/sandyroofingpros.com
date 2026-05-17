# Move Reference Website Screenshots from Downloads to this folder
# Right-click this file and choose "Run with PowerShell"

$source = "$env:USERPROFILE\Downloads"
$dest = Split-Path -Parent $MyInvocation.MyCommand.Path

$files = @(
    "1_StGeorgeConcrete_screenshot.jpg",
    "2_BentonvilleConcrete_screenshot.jpg",
    "3_IrvingTXCarpetCleaning_screenshot.jpg"
)

$moved = 0
foreach ($file in $files) {
    $from = Join-Path $source $file
    $to   = Join-Path $dest $file
    if (Test-Path $from) {
        Move-Item -Path $from -Destination $to -Force
        Write-Host "✅ Moved: $file"
        $moved++
    } else {
        Write-Host "⚠️  Not found in Downloads: $file"
    }
}

Write-Host ""
Write-Host "$moved of $($files.Count) files moved to:"
Write-Host $dest
Write-Host ""
Write-Host "Press any key to close..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
