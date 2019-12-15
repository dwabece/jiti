from jiti.worklogs import UserWorklog


def test_add():
    # today = datetime.date.today()
    uw = UserWorklog()
    uw.pushHours('2011-11-10', 10)
    uw.pushHours('2011-11-10', 15)
    uw.pushHours('2011-11-13', 15)

    assert uw.__dict__['2011-11-10'] == 25
    assert uw.__dict__['2011-11-13'] == 15
