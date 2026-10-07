$dir = 'D:\software\growth\code\personal-knowledge-backend\md'
$files = Get-ChildItem -Path $dir -Filter '*.md' | Where-Object { $_.Name -match '_' }

foreach ($file in $files) {
    Write-Host "=== $($file.Name) ==="
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    $content = [System.Text.Encoding]::UTF8.GetString($bytes)

    $headings = [regex]::Matches($content, '(?m)^#{1,6} .+')
    foreach ($h in $headings) {
        Write-Host $h.Value
    }

    $mermaidCount = ([regex]::Matches($content, '```mermaid')).Count
    $codeCount = ([regex]::Matches($content, '```')).Count
    Write-Host "--- Code blocks: $codeCount, Mermaid: $mermaidCount ---"
    Write-Host ""
}