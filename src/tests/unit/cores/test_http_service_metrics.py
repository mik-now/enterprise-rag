# Copyright (C) 2024-2026 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from comps.cores.mega.http_service import HTTPService


def _routes(service):
    return {route.path for route in service.app.routes}


def test_metrics_on_the_api_port_without_metrics_port(monkeypatch):
    monkeypatch.delenv("METRICS_PORT", raising=False)
    assert "/metrics" in _routes(HTTPService())


def test_metrics_off_the_api_port_with_metrics_port(monkeypatch):
    monkeypatch.setenv("METRICS_PORT", "9464")
    assert "/metrics" not in _routes(HTTPService())
