from app import get_answer


def test_get_answer():
    phrases = ['', 'The weather is nice.', '12', '@']
    for phrase in phrases:
        assert type(get_answer(phrase)) is str


if __name__ == '__main__':
    test_get_answer()

