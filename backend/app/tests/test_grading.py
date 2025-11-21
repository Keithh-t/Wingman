from services.grading import grade_answer

def test_grade_answer_exact_match():
    assert grade_answer("F = ma", "F = ma") is True

def test_grade_answer_ignores_whitespace_and_case():
    assert grade_answer("  f   = MA  ", "F = ma") is True

def test_grade_answer_incorrect():
    assert grade_answer("F = 2ma", "F = ma") is False