import argparse


def run(panama_ratio=None, suez_ratio=None):
    """Run the LNG trade flow simulation and return results as a string."""
    lines = []
    lines.append(f"Panama Canal Usage Ratio: {panama_ratio}")
    lines.append(f"Suez Canal Usage Ratio: {suez_ratio}")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LNG trade flow simulation')
    parser.add_argument('--panama_ratio', type=float, default=None,
                        help='Panama canal usage ratio (0-1) applied to all port pairs')
    parser.add_argument('--suez_ratio', type=float, default=None,
                        help='Suez canal usage ratio (0-1) applied to all port pairs')
    args = parser.parse_args()
    print(run(args.panama_ratio, args.suez_ratio))
