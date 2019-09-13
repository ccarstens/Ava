import logging



logging.basicConfig(filename="logs/tests.log", level=logging.DEBUG,
                    format='%(asctime)s | %(process)d | %(levelname)s | %(message)s')


def test_first_test():
    x = 5
    assert x == 5, "Failed because x is 3"