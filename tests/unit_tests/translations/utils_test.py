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

from unittest.mock import mock_open, patch

from superset.translations.utils import ALL_LANGUAGE_PACKS, get_language_pack
from superset.utils import json


def test_get_language_pack_returns_cached_en() -> None:
    ALL_LANGUAGE_PACKS["en"] = {"hello": "hello"}
    try:
        result = get_language_pack("en")
        assert result == {"hello": "hello"}
    finally:
        ALL_LANGUAGE_PACKS["en"] = {}


def test_get_language_pack_loads_from_file() -> None:
    pack_data = {"Dashboard": "Tableau de bord"}
    ALL_LANGUAGE_PACKS.pop("fr", None)
    try:
        with patch(
            "builtins.open",
            mock_open(read_data=json.dumps(pack_data)),
        ):
            result = get_language_pack("fr")
        assert result == pack_data
        assert ALL_LANGUAGE_PACKS["fr"] == pack_data
    finally:
        ALL_LANGUAGE_PACKS.pop("fr", None)


def test_get_language_pack_caches_result() -> None:
    pack_data = {"Charts": "Graphiques"}
    ALL_LANGUAGE_PACKS["de"] = pack_data
    try:
        result = get_language_pack("de")
        assert result is pack_data
    finally:
        ALL_LANGUAGE_PACKS.pop("de", None)


def test_get_language_pack_falls_back_to_en_on_error() -> None:
    ALL_LANGUAGE_PACKS["en"] = {"fallback": True}
    ALL_LANGUAGE_PACKS.pop("xx", None)
    try:
        with patch("builtins.open", side_effect=FileNotFoundError("not found")):
            result = get_language_pack("xx")
        assert result == {"fallback": True}
    finally:
        ALL_LANGUAGE_PACKS["en"] = {}


def test_get_language_pack_empty_locale_uses_empty_pack() -> None:
    ALL_LANGUAGE_PACKS["en"] = {}
    ALL_LANGUAGE_PACKS.pop("", None)
    try:
        pack_data = {"empty_locale": True}
        with patch(
            "builtins.open",
            mock_open(read_data=json.dumps(pack_data)),
        ):
            result = get_language_pack("")
        assert result == pack_data
    finally:
        ALL_LANGUAGE_PACKS.pop("", None)


def test_get_language_pack_en_locale_uses_empty_pack_file() -> None:
    ALL_LANGUAGE_PACKS.pop("en", None)
    try:
        pack_data = {"en_pack": True}
        with patch(
            "builtins.open",
            mock_open(read_data=json.dumps(pack_data)),
        ) as m:
            result = get_language_pack("en")
        assert result == pack_data
        opened_path: str = m.call_args[0][0]
        assert "empty_language_pack.json" in opened_path
    finally:
        ALL_LANGUAGE_PACKS["en"] = {}
