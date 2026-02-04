
from app.events import check_date_passed

def test_date_is_passed():
  assert check_date_passed("2021-01-01") is True