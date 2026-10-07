$dir = 'D:\software\growth\code\personal-knowledge-backend\md'
$file = Get-ChildItem -Path $dir -Filter '2_*.md' | Select-Object -First 1
$path = $file.FullName

Write-Host "Processing: $path"
Write-Host "Original size: $((Get-Item $path).Length) bytes"

$content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

$lines = $content -split "`n"
$newLines = New-Object System.Collections.Generic.List[string]

for ($i = 0; $i -lt $lines.Length; $i++) {
    if ($lines[$i].Trim() -eq '---') {
        if ($newLines.Count -gt 0 -and $newLines[$newLines.Count - 1].Trim() -eq '') {
            $newLines.RemoveAt($newLines.Count - 1)
        }
        if (($i + 1) -lt $lines.Length -and $lines[$i + 1].Trim() -eq '') {
            $i++
        }
        continue
    }
    $newLines.Add($lines[$i])
}

$content = $newLines -join "`n"
$content = [regex]::Replace($content, "`n{3,}", "`n`n")
$content = [regex]::Replace($content, "[ \t]+`n", "`n")

[System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)

Write-Host "New size: $((Get-Item $path).Length) bytes"
$lines2 = $content -split "`n"
Write-Host "Total lines: $($lines2.Length)"
$blanks = 0
foreach ($l in $lines2) { if ($l.Trim() -eq '') { $blanks++ } }
Write-Host "Blank lines: $blanks"