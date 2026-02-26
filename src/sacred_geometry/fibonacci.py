"""
Fibonacci sequence implementation for natural proportions.
The Fibonacci sequence appears throughout nature and architecture.
"""

from typing import List
import numpy as np


class FibonacciSequence:
    """Generate and work with Fibonacci numbers."""
    
    @staticmethod
    def generate(n: int) -> List[int]:
        """
        Generate first n Fibonacci numbers.
        
        Args:
            n: Number of terms to generate
            
        Returns:
            List of Fibonacci numbers
        """
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        elif n == 2:
            return [0, 1]
        
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        
        return fib
    
    @staticmethod
    def nth_term(n: int) -> int:
        """
        Calculate the nth Fibonacci number using Binet's formula.
        
        Args:
            n: Index of term (0-indexed)
            
        Returns:
            nth Fibonacci number
        """
        phi = (1 + np.sqrt(5)) / 2
        psi = (1 - np.sqrt(5)) / 2
        return int((phi**n - psi**n) / np.sqrt(5))
    
    @staticmethod
    def ratios(n: int) -> List[float]:
        """
        Calculate ratios between consecutive Fibonacci numbers.
        Converges to golden ratio.
        
        Args:
            n: Number of ratios to calculate
            
        Returns:
            List of ratios
        """
        fib = FibonacciSequence.generate(n + 1)
        ratios = []
        
        for i in range(1, len(fib)):
            if fib[i-1] != 0:
                ratios.append(fib[i] / fib[i-1])
        
        return ratios
    
    @staticmethod
    def fibonacci_spiral_squares(n: int) -> List[dict]:
        """
        Generate square dimensions for Fibonacci spiral visualization.
        
        Args:
            n: Number of squares
            
        Returns:
            List of dictionaries with square properties
        """
        fib = FibonacciSequence.generate(n + 2)
        squares = []
        x, y = 0, 0
        
        # Direction: right, up, left, down
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        dir_idx = 0
        
        for i in range(2, len(fib)):
            size = fib[i]
            squares.append({
                'x': x,
                'y': y,
                'size': size,
                'index': i - 2
            })
            
            # Move to next position
            dx, dy = directions[dir_idx % 4]
            if dir_idx % 4 == 0:  # right
                x += size
            elif dir_idx % 4 == 1:  # up
                y += size
            elif dir_idx % 4 == 2:  # left
                x -= size
            else:  # down
                y -= size
            
            dir_idx += 1
        
        return squares
