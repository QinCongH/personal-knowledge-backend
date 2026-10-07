$dir = 'D:\software\growth\code\personal-knowledge-backend\md'
$files = Get-ChildItem -Path $dir -Filter '*.md' | Where-Object { $_.Name -like '*RAG*' }
foreach ($file in $files) {
    Write-Host "=== File: $($file.Name) ==="
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    $content = [System.Text.Encoding]::UTF8.GetString($bytes)
    $lines = $content -split "`n"
    Write-Host "Total lines: $($lines.Length)"
    
    # Count 3+ consecutive newlines
    $matches = [regex]::Matches($content, "`n{3,}")
    Write-Host "3+ consecutive newlines count: $($matches.Count)"
    
    # Find locations with 2+ blank lines
    $blankCount = 0
    $excessFound = $false
    for ($i = 0; $i -lt $lines.Length; $i++) {
        if ($lines[$i].Trim() -eq '') {
            $blankCount++
        } else {
            if ($blankCount -ge 2) {
                Write-Host "  Lines $($i - $blankCount + 1)-$($i) have $blankCount blank lines"
                $excessFound = $true
            }
            $blankCount = 0
        }
    }
    if (-not $excessFound) {
        Write-Host "  No 2+ consecutive blank lines found."
    }
}