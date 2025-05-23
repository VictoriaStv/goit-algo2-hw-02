from typing import List, Dict
from dataclasses import dataclass
import itertools

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    jobs = [PrintJob(**job) for job in print_jobs]
    jobs.sort(key=lambda job: job.priority) 
    print_order = []
    total_time = 0
    used = [False] * len(jobs)

    while not all(used):
        current_group = []
        current_volume = 0
        count = 0
        for i, job in enumerate(jobs):
            if not used[i] and count < constraints["max_items"] and current_volume + job.volume <= constraints["max_volume"]:
                current_group.append(job)
                current_volume += job.volume
                count += 1
                used[i] = True

        print_order.extend([job.id for job in current_group])
        if current_group:
            total_time += max(job.print_time for job in current_group)

    return {
        "print_order": print_order,
        "total_time": total_time
    }


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(n):
        if n == 0:
            return 0, []
        max_val = 0
        best_cut = []
        for i in range(1, n+1):
            if i <= len(prices):
                val, cut = dp(n - i)
                candidate = cut + [i]
                if prices[i-1] + val > max_val or (prices[i-1] + val == max_val and candidate < best_cut):
                    max_val = prices[i-1] + val
                    best_cut = candidate
        return max_val, best_cut

    max_profit, cuts = dp(length)
    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    dp = [0] * (length + 1)
    cut_track = [[] for _ in range(length + 1)]

    for i in range(1, length + 1):
        for j in range(1, i + 1):
            if j <= len(prices):
                if dp[i] < dp[i - j] + prices[j - 1]:
                    dp[i] = dp[i - j] + prices[j - 1]
                    cut_track[i] = cut_track[i - j] + [j]

    return {
        "max_profit": dp[length],
        "cuts": cut_track[length],
        "number_of_cuts": len(cut_track[length]) - 1
    }


def run_tests():
    test_cases = [
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")

if __name__ == "__main__":
    run_tests()

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print_jobs_1 = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    print_jobs_2 = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
    ]

    print_jobs_3 = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    print("\nТест 1 (однаковий пріоритет):")
    result1 = optimize_printing(print_jobs_1, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(print_jobs_2, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(print_jobs_3, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")
