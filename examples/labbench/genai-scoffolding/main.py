"""
This module calculates the sum of numbers from 1 to n,
where n is a positive integer provided as user input.
"""

def compute_sum(n: int) -> int:
    """
    Computes the sum of numbers from 1 to n.

    Args:
        n: A positive integer.

    Returns:
        The sum of numbers from 1 to n.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer.")

    return sum(range(1, n + 1))


if __name__ == "__main__":
    try:
        n = int(input("Enter a positive integer: "))
        result = compute_sum(n)
        print(f"The sum of numbers from 1 to {n} is: {result}")
    except ValueError:
        print("Invalid input. Please enter a positive integer.")
