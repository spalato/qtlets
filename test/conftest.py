import pytest

from PySide2.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication([])
    return app