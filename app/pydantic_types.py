# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0

from typing import TYPE_CHECKING, Any, Optional, no_type_check

from pydantic.errors import UrlHostError, UrlPortError
from pydantic.fields import ModelField
from pydantic.main import BaseConfig
from pydantic.networks import ascii_domain_regex, int_domain_regex
from pydantic.validators import str_validator

if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator


class Port(int):
    @no_type_check
    def __new__(cls, port: Optional[int], **kwargs) -> object:
        return int.__new__(cls, cls.build(**kwargs) if port is None else port)

    def __init__(self, port: int, *args, **kwargs) -> None:
        int.__init__(port)

    @classmethod
    def build(cls, port: int, *args, **kwargs) -> int:
        return port

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value: Any, field: ModelField, config: BaseConfig) -> "Port":
        if value.__class__ == cls:
            return value

        port = value
        if port is not None and port > 65_535:
            raise UrlPortError()

        return cls(port)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"


class Domain(str):
    strip_whitespace = True

    @no_type_check
    def __new__(cls, domain: Optional[str], **kwargs) -> object:
        return str.__new__(cls, cls.build(**kwargs) if domain is None else domain)

    def __init__(self, domain: str, *args, **kwargs) -> None:
        str.__init__(domain)

    @classmethod
    def build(cls, domain: str, *args, **kwargs) -> str:
        return domain

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value: Any, field: ModelField, config: BaseConfig) -> "Domain":
        if value.__class__ == cls:
            return value

        value = str_validator(value)
        if cls.strip_whitespace:
            value = value.strip()

        host = value

        is_international = False
        d = ascii_domain_regex().fullmatch(host)
        if d is None:
            d = int_domain_regex().fullmatch(host)
            if d is None:
                raise UrlHostError()
            is_international = True

        tld = d.group("tld")
        if tld is None and not is_international:
            is_international = True

        if is_international:
            host = host.encode("idna").decode("ascii")

        return cls(host)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"