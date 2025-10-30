def grade_answer(user_answer: str, solution: str) -> bool:
    # MVP, text-only, lenient whitespace/case
    a = " ".join(user_answer.split()).strip().lower()
    b = " ".join(solution.split()).strip().lower()
    return a == b