import subprocess
import time


def find_net_device() -> list[str]:
    cmd: list[str] = "netsh interface ipv4 show interfaces".split()
    final_result: list[str] = []

    result = subprocess.run(
        cmd,
        universal_newlines=True,
        check=False,
        encoding="cp737",
        stdout=subprocess.PIPE,
    )
    result = result.stdout
    result = result.split("connected")

    for temp_res in result:
        temp_res = temp_res.split("\n")[0]
        temp_res = temp_res.strip()
        if "Loopback" in temp_res:
            temp_res = ""
        final_result.append(temp_res)

    final_result = list(filter(None, final_result))

    if not final_result:
        final_result = ["No devices"]

    return final_result[::-1]


def run_command(cmd: list[str]) -> bool:
    result = subprocess.run(
        cmd, check=False, encoding="cp737", stdout=subprocess.DEVNULL
    )
    return not bool(result.returncode)


def change_to_staticip(device_name: str, ip_address: str, subnet_mask: str, gateway: str) -> bool:

    cmd: list[str] = [
        "netsh",
        "interface",
        "ipv4",
        "set",
        "address",
        device_name,
        "static",
        ip_address,
        subnet_mask,
        gateway,
    ]

    return run_command(cmd)


def change_to_dhcp(device_name: str | list[str]) -> bool:

    if isinstance(device_name, list):
        device_name = device_name[0]

    cmd: list[str] = [
        "netsh",
        "interface",
        "ipv4",
        "set",
        "address",
        device_name,
        "source=dhcp",
    ]

    return run_command(cmd)

def change_to_staticdns(device_name: str, dns_ip_address: str) -> bool:

    cmd: list[str] = [
        "netsh",
        "interface",
        "ipv4",
        "set",
        "dns",
        device_name,
        "static",
        dns_ip_address
    ]

    return run_command(cmd)

def change_dns_to_dhcp(device_name: str | list[str]) -> bool:

    if isinstance(device_name, list):
        device_name = device_name[0]
    
    cmd: list[str] = [
        "netsh",
        "interface",
        "ipv4",
        "set",
        "dns",
        device_name,
        "source=dhcp",
    ]

    return run_command(cmd)

    

def renew_ip():
    cmd1 = ["ipconfig", "/release"]
    cmd2 = ["ipconfig", "/renew"]

    if run_command(cmd1):
        time.sleep(5)
        return run_command(cmd2)
    return False
