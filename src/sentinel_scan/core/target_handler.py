import ipaddress
import socket


def normalize_target(target_input: str) -> list[str]:
    """
    Normalize target input into a list of IP addresses.

    Supports:
    - Single IP
    - CIDR range
    - Domain name
    """

    target_input = target_input.strip()

    # Case 1: Try single IP
    try:
        ip_obj = ipaddress.ip_address(target_input)
        return [str(ip_obj)]
    except ValueError:
        pass

    # Case 2: Try CIDR range
    try:
        network = ipaddress.ip_network(target_input, strict=False)
        return [str(ip) for ip in network.hosts()]
    except ValueError:
        pass

    # Case 3: Try domain resolution
    try:
        resolved_ip = socket.gethostbyname(target_input)
        return [resolved_ip]
    except socket.gaierror:
        pass

    raise ValueError(f"Invalid target input: {target_input}")
