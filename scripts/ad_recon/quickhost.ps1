<#
Usage: .\quickhost.ps1 -OutDir C:\Windows\Temp\recon\MyHost
If OutDir not provided, defaults to C:\Windows\Temp\recon\<hostname>\
If issues "powershell -ExecutionPolicy Bypass -File quickhost.ps1"
#>

param(
  [string]$OutDir = $null
)

# compute default if not provided
if ([string]::IsNullOrWhiteSpace($OutDir)) {
    $hc = $env:COMPUTERNAME
    $OutDir = "C:\Windows\Temp\recon\$hc"
}

# create output folder
try {
    if (-not (Test-Path -Path $OutDir)) {
        New-Item -Path $OutDir -ItemType Directory -Force | Out-Null
    }
} catch {
    Write-Error "Failed to create output folder $OutDir - $_"
    exit 1
}

function Save-Output {
  param(
    [Parameter(Mandatory=$true)][string]$File,
    [Parameter(Mandatory=$true)][scriptblock]$ScriptBlock
  )
  try {
    & $ScriptBlock *>&1 | Out-File -FilePath $File -Encoding utf8 -Width 4096
  } catch {
    "$((Get-Date).ToString('o')) - Failed: $File -> $_" | Out-File -FilePath "$OutDir\errors.txt" -Append
  }
}

Write-Output "Output folder: $OutDir"

# Low-noise initial facts
Save-Output "$OutDir\whoami.txt" { whoami /priv }
Save-Output "$OutDir\whoami_all.txt" { whoami /all }
Save-Output "$OutDir\net_users.txt" { net user }
Save-Output "$OutDir\local_admins.txt" { net localgroup administrators }
Save-Output "$OutDir\systeminfo.txt" { systeminfo }
Save-Output "$OutDir\ipconfig.txt" { ipconfig /all }
Save-Output "$OutDir\nltest_trusts.txt" { nltest /domain_trusts }

# Scheduled tasks & services
Save-Output "$OutDir\schtasks.txt" { schtasks /query /fo LIST /v }
Save-Output "$OutDir\services.txt" { Get-Service | Sort-Object Status,Name | Format-Table -AutoSize }

# Network sessions & shares
Save-Output "$OutDir\shares.txt" { net share }
Save-Output "$OutDir\sessions.txt" { net session }

# PowerView section
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pvPath = Join-Path -Path $scriptDir -ChildPath 'PowerView.ps1'

function Get-DomainFromHost {
    # Try common env vars first
    if ($env:USERDNSDOMAIN -and -not [string]::IsNullOrWhiteSpace($env:USERDNSDOMAIN)) {
        return $env:USERDNSDOMAIN
    }
    if ($env:USERDOMAIN -and -not [string]::IsNullOrWhiteSpace($env:USERDOMAIN)) {
        # USERDOMAIN is NetBIOS name; try to convert to DNS style if possible
        return $env:USERDOMAIN
    }
    # Try WMI/CIM
    try {
        $cs = Get-CimInstance Win32_ComputerSystem -ErrorAction Stop
        if ($cs.Domain -and -not [string]::IsNullOrWhiteSpace($cs.Domain)) {
            return $cs.Domain
        }
    } catch {
        # ignore
    }
    # If AD module is present, ask for the domain
    try {
        Import-Module ActiveDirectory -ErrorAction Stop
        $adDomain = (Get-ADDomain).DNSRoot
        if ($adDomain) { return $adDomain }
    } catch {
        # ignore if AD module not available
    }
    return $null
}

if (Test-Path $pvPath) {
    Write-Output "PowerView detected next to script. Attempting domain detection..."
    $Domain = Get-DomainFromHost
    if (-not $Domain) {
        "$((Get-Date).ToString('o')) - PowerView skipped: Could not detect domain from environment. Consider providing PowerView on a domain-joined account or run with explicit Domain parameter." | Out-File -FilePath "$OutDir\errors.txt" -Append
        Write-Output "PowerView found but domain detection failed. Skipping PowerView queries."
    } else {
        Write-Output "Detected domain: $Domain"
        try {
            Import-Module $pvPath -Force -DisableNameChecking
            # Use explicit -Domain parameter to satisfy functions that require it
            Save-Output "$OutDir\pv_users.txt" { Get-NetUser -Domain $Domain | Select-Object Name,SamAccountName,LastLogonDate }
            Save-Output "$OutDir\pv_computers.txt" { Get-NetComputer -Domain $Domain | Select-Object Name,OperatingSystem,LastLogonDate }
            Save-Output "$OutDir\pv_domainadmins.txt" { Get-DomainGroupMember -Identity 'Domain Admins' -Domain $Domain }
        } catch {
            "$((Get-Date).ToString('o')) - PowerView invocation failed: $_" | Out-File -FilePath "$OutDir\errors.txt" -Append
        }
    }
} else {
    Write-Output "PowerView not found. To run PowerView, place PowerView.ps1 next to this script and re-run."
}

Write-Output "Done. Outputs saved to $OutDir"
