from tasks3 import inc, main


def test_inc_basic():
    assert inc(0) == 1
    assert inc(10) == 11


def test_main_contains_results():
    out = main()
    assert isinstance(out, dict)
    assert out["inc_2"] == 3
    assert out["inc_5"] == 6
