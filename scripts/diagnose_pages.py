"""Read-only Pages diagnostics. Never deploys or changes DNS or repository settings."""
import json
import os
import subprocess
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DOMAINS = ("khetibadibazaar.com", "www.khetibadibazaar.com")
GITHUB_IPS = ("185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153")


def run(*args):
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=20)
        return {"exit_code": result.returncode, "output": result.stdout.strip(), "error": result.stderr.strip()}
    except (subprocess.TimeoutExpired, FileNotFoundError) as error:
        return {"error": type(error).__name__}


def pages_configuration():
    token = os.environ.get("GH_TOKEN")
    repository = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repository:
        return {"unavailable": "Run the manual GitHub Actions workflow to read Pages settings."}
    request = Request(
        f"https://api.github.com/repos/{repository}/pages",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2026-03-10"},
    )
    try:
        with urlopen(request, timeout=15) as response:
            data = json.load(response)
        # Print only public-facing Pages configuration, never request headers/tokens.
        return {key: data.get(key) for key in ("status", "cname", "html_url", "build_type", "https_enforced", "https_certificate", "protected_domain_state", "pending_domain_unverified_at")}
    except HTTPError as error:
        return {"unavailable": f"Pages configuration API returned HTTP {error.code}"}
    except (URLError, TimeoutError, ValueError):
        return {"unavailable": "Pages configuration API could not be read."}


def header_check(domain, scheme="http", ip=None):
    args = ["curl", "--silent", "--show-error", "--head", "--location", "--max-redirs", "5", "--max-time", "15"]
    if ip:
        args.extend(["--resolve", f"{domain}:80:{ip}"])
    args.append(f"{scheme}://{domain}/")
    return run(*args)


def main():
    report = {"pages_configuration": pages_configuration(), "domains": {}}
    for domain in DOMAINS:
        print(f"Checking {domain} from the GitHub runner...", flush=True)
        report["domains"][domain] = {
            "dns": {kind: run("dig", "+time=3", "+tries=1", "+noall", "+answer", domain, kind) for kind in ("A", "AAAA", "CNAME", "CAA", "NS")},
            "google_dns": run("dig", "@8.8.8.8", "+time=3", "+tries=1", "+noall", "+answer", domain, "A"),
            "http": header_check(domain),
            "https": header_check(domain, "https"),
            "direct_github_http": {ip: header_check(domain, ip=ip) for ip in GITHUB_IPS},
        }
    output = json.dumps(report, indent=2)
    print(output)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as stream:
            stream.write("## Custom-domain diagnostics\n\nRead-only checks from GitHub's network. No DNS or Pages settings were changed.\n\n")
            stream.write("The direct-IP checks bypass DNS for HTTP only. HTTPS certificate verification remains enabled.\n\n")
            stream.write("```json\n" + output + "\n```\n")


if __name__ == "__main__":
    main()
