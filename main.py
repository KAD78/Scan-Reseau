
#!/usr/bin/env python3
import asyncio, ipaddress, subprocess, sys, shutil

TIMEOUT = 1
MAX_CONCURRENT = 500

# ================= SCAN =================
async def scan_port(ip, port):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port), timeout=TIMEOUT
        )

        banner = ""

        if port in [80,8080,8000]:
            writer.write(b"GET / HTTP/1.0\r\n\r\n")
            await writer.drain()

        data = await asyncio.wait_for(reader.read(1024), timeout=TIMEOUT)

        if data:
            banner = data.decode(errors="ignore").strip().split("\n")[0][:100]

        writer.close()
        await writer.wait_closed()

        return (port, banner)

    except:
        return None

async def run_scan(target, ports):
    ips = expand_targets(target)
    results = []

    sem = asyncio.Semaphore(MAX_CONCURRENT)

    async def sem_scan(ip, port):
        async with sem:
            return await scan_port(ip, port)

    tasks = []
    for ip in ips:
        for port in ports:
            tasks.append((ip, port, asyncio.create_task(sem_scan(ip, port))))

    for ip, port, task in tasks:
        res = await task
        if res:
            results.append({
                "ip": ip,
                "port": port,
                "banner": res[1]
            })

    return results

def expand_targets(target):
    try:
        net = ipaddress.ip_network(target, strict=False)
        return [str(ip) for ip in net.hosts()]
    except:
        return [target]

# ================= DETECTION =================
def detect_service(port, banner):
    banner = banner.lower()

    if "nginx" in banner:
        return "nginx"
    if "apache" in banner:
        return "apache"
    if "ssh" in banner:
        return "ssh"
    if "ftp" in banner:
        return "ftp"
    if "rtsp" in banner or port == 554:
        return "IP Camera (RTSP)"

    return "Unknown"

# ================= NMAP =================
def run_nmap(ip):
    if not shutil.which("nmap"):
        print("\n[!] Nmap not installed → skipping")
        return

    print("\n[+] Running Nmap (service detection)...\n")

    try:
        result = subprocess.run(
            ["nmap", "-sV", "-Pn", ip],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except Exception as e:
        print(f"[!] Error running Nmap: {e}")

# ================= MAIN =================
def main():
    print("\n=== Network Audit Tool PRO ===\n")

    target = input("Target IP/CIDR: ")
    ports = input("Ports (ex: 22,80,443): ")
    ports = [int(p.strip()) for p in ports.split(",")]

    print("\n[+] Fast scanning...\n")
    results = asyncio.run(run_scan(target, ports))

    if not results:
        print("No open ports found.")
    else:
        print("=== FAST SCAN RESULTS ===\n")

        for r in results:
            service = detect_service(r["port"], r["banner"])
            print(f"[+] {r['ip']}:{r['port']} → {service}")

            if r["banner"]:
                print(f"    Banner: {r['banner']}")

    # ===== NMAP =====
    run = input("\nRun deep scan with Nmap? (y/n): ")

    if run.lower() == "y":
        run_nmap(target)

if __name__ == "__main__":
    main()


"""

#!/usr/bin/env python3
import asyncio, ipaddress, subprocess, sys

TIMEOUT = 1
MAX_CONCURRENT = 500

DEFAULT_CREDS = [
    ("admin","admin"),
    ("admin","password"),
    ("root","root"),
    ("admin","1234")
]

# ===== SCAN =====
async def scan_port(ip, port):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port), timeout=TIMEOUT
        )

        banner = ""

        # HTTP
        if port in [80,8080,8000]:
            writer.write(b"GET / HTTP/1.0\r\n\r\n")
            await writer.drain()

        data = await asyncio.wait_for(reader.read(1024), timeout=TIMEOUT)

        if data:
            banner = data.decode(errors="ignore").strip().split("\n")[0][:100]

        writer.close()
        await writer.wait_closed()

        return (port, banner)

    except:
        return None

async def run_scan(target, ports):
    ips = expand_targets(target)
    results = []

    sem = asyncio.Semaphore(MAX_CONCURRENT)

    async def sem_scan(ip, port):
        async with sem:
            return await scan_port(ip, port)

    tasks = []
    for ip in ips:
        for port in ports:
            tasks.append((ip, port, asyncio.create_task(sem_scan(ip, port))))

    for ip, port, task in tasks:
        res = await task
        if res:
            results.append({
                "ip": ip,
                "port": port,
                "banner": res[1]
            })

    return results

def expand_targets(target):
    try:
        net = ipaddress.ip_network(target, strict=False)
        return [str(ip) for ip in net.hosts()]
    except:
        return [target]

# ===== DETECTION =====
def detect_device(result):
    banner = result["banner"].lower()

    if "ip camera" in banner or "webcam" in banner:
        return "📷 IP Camera"

    if "mikrotik" in banner:
        return "📡 Router MikroTik"

    if "nginx" in banner:
        return "🌐 Web Server (nginx)"

    if "apache" in banner:
        return "🌐 Web Server (Apache)"

    if "ssh" in banner:
        return "🔐 SSH Server"

    return "Unknown"

# ===== DEFAULT CREDS TEST (SAFE) =====
def test_default_http(ip):
    import requests

    for user, pwd in DEFAULT_CREDS:
        try:
            r = requests.get(f"http://{ip}", auth=(user,pwd), timeout=2)
            if r.status_code == 200:
                print(f"[!!!] Default creds found: {user}/{pwd} on {ip}")
                return
        except:
            pass

# ===== EXTERNAL TOOLS =====
def run_nmap(ip):
    print("\n[+] Running Nmap...")
    subprocess.run(["nmap","-sV",ip])

def run_nikto(ip):
    print("\n[+] Running Nikto...")
    subprocess.run(["nikto","-h",ip])

# ===== MAIN =====
def main():
    target = input("Target IP/CIDR: ")
    ports = input("Ports (ex 22,80,443): ")
    ports = [int(p.strip()) for p in ports.split(",")]

    print("\n[+] Scanning...\n")
    results = asyncio.run(run_scan(target, ports))

    for r in results:
        device = detect_device(r)
        print(f"{r['ip']}:{r['port']} → {device}")
        if r["banner"]:
            print(f"   Banner: {r['banner']}")

    # ===== TEST DEFAULT CREDS =====
    print("\n[+] Testing default credentials (HTTP)...")
    for r in results:
        if r["port"] == 80:
            test_default_http(r["ip"])

    # ===== TOOLS =====
    use_tools = input("\nRun advanced tools? (y/n): ")
    if use_tools.lower() == "y":
        run_nmap(target)
        run_nikto(target)

if __name__ == "__main__":
    main()

"""
