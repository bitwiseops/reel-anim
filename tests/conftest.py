import pytest


@pytest.fixture(autouse=True, scope="session")
def _manim_fuori_dal_progetto(tmp_path_factory):
    """Le scene costruite nei test scrivono i loro file in una cartella temporanea, non in ./media."""
    from manim import config
    config.media_dir = str(tmp_path_factory.mktemp("manim"))
