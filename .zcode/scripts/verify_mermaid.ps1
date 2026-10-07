$dir = 'D:\software\growth\code\personal-knowledge-backend\md'
$files = Get-ChildItem -Path $dir -Filter '*.md' | Where-Object { $_.Name -match '^[123]_' }
$totalMermaid = 0

foreach ($file in $files) {
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    $content = [System.Text.Encoding]::UTF8.GetString($bytes)

    $regex = New-Object System.Text.RegularExpressions.Regex('```mermaid\s*\r?\n(.*?)```', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    $matches = $regex.Matches($content)

    Write-Host "=== $($file.Name) ==="
    Write-Host "Mermaid blocks: $($matches.Count)"
    $idx = 0
    foreach ($m in $matches) {
        $idx++
        $block = $m.Groups[1].Value
        $lines = $block -split "`n"
        Write-Host "  --- Block $idx ($($lines.Length) lines) ---"

        $issues = @()
        for ($i = 0; $i -lt $lines.Length; $i++) {
            $line = $lines[$i]
            $stringMatches = [regex]::Matches($line, '"([^"]*)"')
            foreach ($sm in $stringMatches) {
                $str = $sm.Groups[1].Value
                if ($str -match '\(') { $issues += "L$($i+1): '(' in string" }
                if ($str -match '\[') { $issues += "L$($i+1): '[' in string" }
                if ($str -match "'") { $issues += "L$($i+1): single quote in string" }
            }
        }
        if ($issues.Count -eq 0) {
            Write-Host "  OK"
        } else {
            foreach ($issue in $issues) {
                Write-Host "  WARN: $issue"
            }
        }
    }
    Write-Host ""
    $totalMermaid += $matches.Count
}

Write-Host "Total mermaid blocks: $totalMermaid"