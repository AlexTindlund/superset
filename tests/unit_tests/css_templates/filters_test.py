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

from unittest.mock import MagicMock

from superset.css_templates.filters import CssTemplateAllTextFilter


def _make_filter() -> CssTemplateAllTextFilter:
    mock_model = MagicMock()
    return CssTemplateAllTextFilter(mock_model, mock_model)


def test_filter_returns_query_unchanged_for_empty_value() -> None:
    mock_query = MagicMock()
    filter_instance = _make_filter()
    result = filter_instance.apply(mock_query, "")
    assert result is mock_query
    mock_query.filter.assert_not_called()


def test_filter_returns_query_unchanged_for_none_value() -> None:
    mock_query = MagicMock()
    filter_instance = _make_filter()
    result = filter_instance.apply(mock_query, None)
    assert result is mock_query
    mock_query.filter.assert_not_called()


def test_filter_applies_filter_for_nonempty_value() -> None:
    mock_query = MagicMock()
    filter_instance = _make_filter()
    result = filter_instance.apply(mock_query, "test")
    mock_query.filter.assert_called_once()
    assert result is mock_query.filter.return_value


def test_filter_has_correct_name() -> None:
    filter_instance = _make_filter()
    assert filter_instance.arg_name == "css_template_all_text"
