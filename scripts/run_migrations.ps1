param(
    [string] $DatabaseUrl = "postgresql://sourcematch:sourcematchpass@localhost:5432/sourcematch"
)

Write-Host "Setting DATABASE_URL for this session..."
$env:DATABASE_URL = $DatabaseUrl
Write-Host "DATABASE_URL set to: $env:DATABASE_URL"

Write-Host "Creating alembic revision (autogenerate)..."
alembic revision --autogenerate -m "initial"

Write-Host "Applying migrations (upgrade head)..."
alembic upgrade head

Write-Host "Migrations complete."
