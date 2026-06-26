# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from __future__ import annotations

from superset.temporary_cache.utils import cache_key, SEPARATOR


def test_cache_key_single_arg() -> None:
    assert cache_key("dashboard") == "dashboard"


def test_cache_key_multiple_args() -> None:
    assert cache_key("dashboard", 1, "filter") == "dashboard;1;filter"


def test_cache_key_no_args() -> None:
    assert cache_key() == ""


def test_cache_key_with_none() -> None:
    assert cache_key("a", None, "b") == "a;None;b"


def test_cache_key_with_integers() -> None:
    assert cache_key(1, 2, 3) == "1;2;3"


def test_cache_key_uses_separator() -> None:
    result = cache_key("x", "y")
    assert SEPARATOR in result
    assert result == f"x{SEPARATOR}y"


def test_cache_key_with_empty_string_arg() -> None:
    assert cache_key("", "b") == ";b"


def test_cache_key_with_special_characters() -> None:
    assert cache_key("a/b", "c?d") == "a/b;c?d"
