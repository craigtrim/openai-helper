from openai_helper import __version__


from openai_helper.bp import OpenAIHelper


def test_version():
    assert __version__ == '0.1.0'


def test_bp():

    bp = OpenAIHelper()
    assert bp


def main():
    test_bp()


if __name__ == "__main__":
    main()
