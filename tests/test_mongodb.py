from network_security.db.mongodb import check_mongodb_health


def test_mongodb_health_check_is_safe_without_required_uri():
    health = check_mongodb_health(required=False)
    assert "status" in health
