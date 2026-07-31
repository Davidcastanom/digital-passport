from streamlit.testing.v1 import AppTest


class TestNavigation:
    def test_no_duplicate_keys_when_landing_skipped(self):
        at = AppTest.from_file("app/main.py", default_timeout=30)
        at.session_state["landing"] = False
        at.run()
        assert not at.exception

    def test_three_group_selectboxes(self):
        at = AppTest.from_file("app/main.py", default_timeout=30)
        at.session_state["landing"] = False
        at.run()
        assert not at.exception
        groups = [s.label for s in at.sidebar.selectbox]
        assert len(groups) == 4
        assert "📋 Gestión" in groups
        assert "💼 Datos del Perfil" in groups
        assert "🔍 Exploración" in groups

    def test_navigate_to_register(self):
        at = AppTest.from_file("app/main.py", default_timeout=30)
        at.session_state["landing"] = False
        at.run()
        assert not at.exception
        at.sidebar.selectbox[0].select("Registrar Usuario")
        at.run()
        assert not at.exception
