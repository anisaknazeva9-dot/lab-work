from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError


class Customer:
    def __init__(self, customer_id, name, category, online_consent=False):
        identifier(customer_id)
        name = name.strip()
        choice(category, ("STANDARD", "PREMIUM", "BUSINESS"), "INVALID_CATEGORY")
        boolean(online_consent)
        self._customer_id = customer_id
        cleaned_name = name.strip()
        if not cleaned_name:
            raise DomainError("INVALID_NAME")
        self._name = cleaned_name
        self._category = category
        self._online_consent = online_consent
        self._status = "ACTIVE"

    @property
    def customer_id(self):
        return self._customer_id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @property
    def online_consent(self):
        return self._online_consent

    @property
    def status(self):
        return self._status

    def block(self):
        if self._status != "ACTIVE":
            raise DomainError("INVALID_STATE")
        self._status = "BLOCKED"

    def activate(self):
        if self._status != "BLOCKED":
            raise DomainError("INVALID_STATE")
        self._status = "ACTIVE"
        
    def close(self):
        if self._status not in ("ACTIVE", "BLOCKED"):
            raise DomainError("INVALID_STATE")
        self._status = "CLOSED"

    def availability(self):
        if self._status == "ACTIVE":
            return CheckResult(True)
        if self._status == "BLOCKED":
            return CheckResult(False, "CUSTOMER_BLOCKED")
        if self._status == "CLOSED":
            return CheckResult(False, "CUSTOMER_CLOSED")

    def rename(self, name):
        cleaned = name.strip()
        if not cleaned:
            raise DomainError("INVALID_NAME")
        self._name = cleaned
        
