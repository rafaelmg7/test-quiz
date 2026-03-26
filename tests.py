import pytest
from model import Question


@pytest.fixture
def question_with_multiple_choices():
    question = Question(title="q1", max_selections=3)
    question.add_choice("a", True)
    question.add_choice("b", False)
    question.add_choice("c", True)
    return question


def test_create_question():
    question = Question(title="q1")
    assert question.id != None


def test_create_multiple_questions():
    question1 = Question(title="q1")
    question2 = Question(title="q2")
    assert question1.id != question2.id


def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title="")
    with pytest.raises(Exception):
        Question(title="a" * 201)
    with pytest.raises(Exception):
        Question(title="a" * 500)


def test_create_question_with_valid_points():
    question = Question(title="q1", points=1)
    assert question.points == 1
    question = Question(title="q1", points=100)
    assert question.points == 100


def test_create_choice():
    question = Question(title="q1")

    question.add_choice("a", False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == "a"
    assert not choice.is_correct


def test_create_question_with_invalid_points_below_range():
    with pytest.raises(Exception):
        Question(title="q1", points=0)
    with pytest.raises(Exception):
        Question(title="q1", points=-1)


def test_create_question_with_invalid_points_above_range():
    with pytest.raises(Exception):
        Question(title="q1", points=101)
    with pytest.raises(Exception):
        Question(title="q1", points=500)


def test_add_choice_with_invalid_empty_text():
    question = Question(title="q1")

    with pytest.raises(Exception):
        question.add_choice("", False)


def test_add_choice_with_invalid_long_text():
    question = Question(title="q1")

    with pytest.raises(Exception):
        question.add_choice("a" * 101, False)


def test_add_choice_returns_created_choice():
    question = Question(title="q1")

    choice = question.add_choice("a", True)

    assert choice == question.choices[-1]
    assert choice.text == "a"
    assert choice.is_correct


def test_add_multiple_choices_increment_ids():
    question = Question(title="q1")

    question.add_choice("a", False)
    question.add_choice("b", False)
    question.add_choice("c", False)

    assert [choice.id for choice in question.choices] == [1, 2, 3]


def test_remove_choice_by_id():
    question = Question(title="q1")

    question.add_choice("a", False)
    question.add_choice("b", False)
    question.add_choice("c", False)

    question.remove_choice_by_id(2)

    assert len(question.choices) == 2
    assert [choice.id for choice in question.choices] == [1, 3]


def test_remove_choice_by_invalid_id():
    question = Question(title="q1")

    question.add_choice("a", False)

    with pytest.raises(Exception):
        question.remove_choice_by_id(999)


def test_remove_all_choices():
    question = Question(title="q1")

    question.add_choice("a", False)
    question.add_choice("b", False)
    question.add_choice("c", False)

    question.remove_all_choices()

    assert len(question.choices) == 0


def test_set_correct_choices_and_correct_selected_choices():
    question = Question(title="q1", max_selections=4)

    question.add_choice("a", True)
    question.add_choice("b", False)
    question.add_choice("c", False)

    question.set_correct_choices([3])

    assert question.choices[0].is_correct
    assert not question.choices[1].is_correct
    assert question.choices[2].is_correct
    assert question.correct_selected_choices([1, 2, 3, 999]) == [1, 3]


def test_correct_selected_choices_with_fixture(question_with_multiple_choices):
    correct_selected_choices = question_with_multiple_choices.correct_selected_choices([1, 2, 3])
    assert correct_selected_choices == [1, 3]


def test_correct_selected_choices_exceeds_max_with_fixture(question_with_multiple_choices):
    with pytest.raises(Exception):
        question_with_multiple_choices.correct_selected_choices([1, 2, 3, 999])
