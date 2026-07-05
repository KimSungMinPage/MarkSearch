from app.ui.collection_tab import CollectionTab

def test_collection_tab_does_not_override_tkinter_internal_options():
    assert '_options' not in CollectionTab.__dict__
    assert 'build_options' in CollectionTab.__dict__
