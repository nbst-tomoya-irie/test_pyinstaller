import argparse


def run(panama_ratio=None, suez_ratio=None, nav_speed=None, utilization=None):
    """Run the LNG trade flow simulation and return results as a string."""
    lines = []
    lines.append(f"Panama Canal Usage Ratio: {panama_ratio:.2f}" if panama_ratio is not None else "Panama Canal Usage Ratio: N/A")
    lines.append(f"Suez Canal Usage Ratio: {suez_ratio:.2f}" if suez_ratio is not None else "Suez Canal Usage Ratio: N/A")
    lines.append(f"Ave. Nav Speed: {nav_speed:.2f}" if nav_speed is not None else "Ave. Nav Speed: N/A")
    lines.append(f"Utilization: {utilization:.2f}" if utilization is not None else "Utilization: N/A")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LNG trade flow simulation')
    parser.add_argument('--panama_ratio', type=float, default=None,
                        help='Panama canal usage ratio (0-1) applied to all port pairs')
    parser.add_argument('--suez_ratio', type=float, default=None,
                        help='Suez canal usage ratio (0-1) applied to all port pairs')
    parser.add_argument('--nav_speed', type=float, default=None,
                        help='Average navigation speed (0-100)')
    parser.add_argument('--utilization', type=float, default=None,
                        help='Utilization (0-1)')
    args = parser.parse_args()
    print(run(args.panama_ratio, args.suez_ratio, args.nav_speed, args.utilization))
