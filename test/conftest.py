import pytest

from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication([])
    return app