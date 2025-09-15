$BaseUrl = "http://127.0.0.1:5000/sales"

function Show-Menu {
    Write-Host ""
    Write-Host "--- ETL API Tool ---"
    Write-Host "1. GET all sales"
    Write-Host "2. GET sale by customer_id"
    Write-Host "3. POST (add new sale)"
    Write-Host "4. PUT (update sale by customer_id)"
    Write-Host "5. DELETE sale by customer_id"
    Write-Host "6. Export sales (CSV or Excel)"
    Write-Host "0. Exit"
}

function Get-AllSales {
    $resp = Invoke-RestMethod -Uri $BaseUrl -Method GET
    $resp | Format-Table
}

function Get-SaleByCustomer {
    $cid = Read-Host "Enter customer_id"
    $resp = Invoke-RestMethod -Uri "$BaseUrl/$cid" -Method GET
    $resp | Format-Table
}

function Add-Sale {
    $sale = @{
        date = Read-Host "Date (YYYY-MM-DD)"
        customer_id = [int](Read-Host "Customer ID")
        product = Read-Host "Product"
        quantity = [int](Read-Host "Quantity")
        unit_price = [float](Read-Host "Unit Price")
    }
    $resp = Invoke-RestMethod -Uri $BaseUrl -Method POST -Body ($sale | ConvertTo-Json) -ContentType "application/json"
    $resp
}

function Update-Sale {
    $cid = Read-Host "Enter customer_id to update"
    $update = @{
        quantity = [int](Read-Host "New quantity")
        unit_price = [float](Read-Host "New unit price")
    }
    $resp = Invoke-RestMethod -Uri "$BaseUrl/$cid" -Method PUT -Body ($update | ConvertTo-Json) -ContentType "application/json"
    $resp
}

function Delete-Sale {
    $cid = Read-Host "Enter customer_id to delete"
    $resp = Invoke-RestMethod -Uri "$BaseUrl/$cid" -Method DELETE
    $resp
}

function Export-Sales {
    $fmt = Read-Host "Format (csv/excel)"
    $resp = Invoke-RestMethod -Uri "$BaseUrl/export/$fmt" -Method GET
    $resp
}

# Main loop
do {
    Show-Menu
    $choice = Read-Host "Choose option"

    switch ($choice) {
        "1" { Get-AllSales }
        "2" { Get-SaleByCustomer }
        "3" { Add-Sale }
        "4" { Update-Sale }
        "5" { Delete-Sale }
        "6" { Export-Sales }
        "0" { Write-Host "Exiting..."; break }
        default { Write-Host "Invalid choice. Try again." }
    }
} while ($true)
