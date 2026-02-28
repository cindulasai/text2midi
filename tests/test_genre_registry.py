# -*- coding: utf-8 -*-
"""
Comprehensive tests for the genre registry — the single source of truth
for all genre, scale, and instrument data.
"""

import pytest

from src.config.genre_registry import (
    GENRE_TREE,
    SCALES_EXTENDED,
    SCALE_ALIASES,
    GM_INSTRUMENTS_EXTENDED,
    GenreNode,
    get_genre,
    get_root_genres,
    get_children,
    all_genre_ids,
    get_genre_ids_for_validation,
    get_tempo_ranges,
    find_by_alias,
    get_genre_instruments,
    resolve_scale,
    get_all_scale_names,
)


# =====================================================================
# SECTION 1: Registry Structure Tests
# =====================================================================


class TestRegistryStructure:
    """Verify the registry is well-formed and non-empty."""

    def test_genre_tree_not_empty(self):
        assert len(GENRE_TREE) > 0

    def test_root_genres_minimum(self):
        """We should have at least the 16 root genres."""
        roots = get_root_genres()
        assert len(roots) >= 16

    def test_all_root_ids_present(self):
        expected = {
            "pop", "rock", "metal", "electronic", "hiphop", "jazz",
            "blues", "rnb", "folk", "latin", "african", "asian",
            "classical", "lofi", "ambient", "cinematic",
        }
        roots = {g.id for g in get_root_genres()}
        assert expected.issubset(roots)

    def test_genre_node_is_frozen(self):
        node = get_genre("pop")
        assert node is not None
        with pytest.raises(Exception):
            node.id = "changed"  # type: ignore

    def test_every_genre_has_tempo_range(self):
        for gid in all_genre_ids():
            node = get_genre(gid)
            assert node is not None, f"get_genre('{gid}') returned None"
            lo, hi = node.tempo_range
            assert lo < hi, (
                f"Genre '{gid}' has invalid tempo range: {lo}-{hi}"
            )

    def test_every_genre_has_default_scale(self):
        for gid in all_genre_ids():
            node = get_genre(gid)
            assert node is not None
            assert node.default_scale, f"Genre '{gid}' has no default_scale"

    def test_sub_genres_reference_valid_parent(self):
        """Every dotted genre ID should have a valid root."""
        for gid in all_genre_ids():
            if "." in gid:
                root = gid.split(".")[0]
                assert root in GENRE_TREE, f"Sub-genre '{gid}' has missing root '{root}'"


# =====================================================================
# SECTION 2: Lookup Function Tests
# =====================================================================


class TestLookupFunctions:
    """Test get_genre, find_by_alias, get_children, etc."""

    def test_get_genre_root(self):
        node = get_genre("jazz")
        assert node is not None
        assert node.id == "jazz"

    def test_get_genre_subgenre(self):
        node = get_genre("electronic.house")
        assert node is not None
        assert node.id == "electronic.house"

    def test_get_genre_nonexistent_returns_none(self):
        assert get_genre("nonexistent") is None

    def test_get_children_pop(self):
        children = get_children("pop")
        assert len(children) >= 5  # at least kpop, jpop, synthpop, etc.
        child_ids = [c.id for c in children]
        assert "pop.kpop" in child_ids

    def test_get_children_leaf_returns_empty(self):
        # lofi has no sub-genres
        children = get_children("lofi")
        assert len(children) == 0

    def test_find_by_alias_dubstep(self):
        result = find_by_alias("dubstep")
        assert result is not None
        assert result.id == "electronic.dubstep"

    def test_find_by_alias_kpop(self):
        # "kpop" may not be an exact alias; "k-pop" is
        result = find_by_alias("k-pop")
        assert result is not None
        assert result.id == "pop.kpop"

    def test_find_by_alias_funk(self):
        """Funk should resolve to rnb.funk."""
        result = find_by_alias("funk")
        assert result is not None
        assert result.id == "rnb.funk"

    def test_find_by_alias_bebop(self):
        """'bebop' should resolve via alias to jazz.bebop."""
        result = find_by_alias("bebop")
        assert result is not None
        assert result.id == "jazz.bebop"

    def test_find_by_alias_nonexistent(self):
        assert find_by_alias("zzzinvalid") is None

    def test_all_genre_ids_has_subgenres(self):
        ids = all_genre_ids()
        assert "pop" in ids
        assert "pop.kpop" in ids
        assert "electronic.house" in ids
        assert len(ids) > 50  # should be well over 100

    def test_get_genre_ids_for_validation_returns_tuple(self):
        ids = get_genre_ids_for_validation()
        assert isinstance(ids, tuple)
        assert "pop" in ids
        assert "electronic.dubstep" in ids


# =====================================================================
# SECTION 3: Tempo / Scale / Instrument Tests
# =====================================================================


class TestTempoScaleInstrument:

    def test_tempo_ranges_all_genres(self):
        ranges = get_tempo_ranges()
        assert "pop" in ranges
        assert "electronic.techno" in ranges
        for gid, (lo, hi) in ranges.items():
            assert lo < hi, f"Genre '{gid}' has bad tempo range"

    def test_scales_extended_not_empty(self):
        assert len(SCALES_EXTENDED) >= 20

    def test_original_8_scales_present(self):
        original = {"major", "minor", "dorian", "mixolydian", "pentatonic_major",
                     "pentatonic_minor", "blues", "harmonic_minor"}
        assert original.issubset(set(SCALES_EXTENDED.keys()))

    def test_world_scales_present(self):
        world = {"hijaz", "phrygian_dominant", "japanese_in", "whole_tone"}
        assert world.issubset(set(SCALES_EXTENDED.keys()))

    def test_scale_intervals_are_valid(self):
        for name, intervals in SCALES_EXTENDED.items():
            assert isinstance(intervals, (list, tuple)), f"Scale '{name}' must be a list or tuple"
            assert len(intervals) >= 5, f"Scale '{name}' has fewer than 5 notes"
            assert intervals[0] == 0, f"Scale '{name}' must start at 0"
            for i in intervals:
                assert 0 <= i < 12, f"Scale '{name}' has out-of-range interval {i}"

    def test_resolve_scale_exact(self):
        # resolve_scale returns the interval list for the scale
        result = resolve_scale("major")
        assert result is not None
        assert result[0] == 0  # starts at root

    def test_resolve_scale_alias(self):
        # "aeolian" should resolve to same intervals as "minor"
        aeolian = resolve_scale("aeolian")
        minor = resolve_scale("minor")
        assert aeolian is not None
        assert minor is not None
        assert aeolian == minor

    def test_resolve_scale_unknown(self):
        assert resolve_scale("zzz_nothing") is None

    def test_get_all_scale_names(self):
        names = get_all_scale_names()
        assert "major" in names
        assert "hijaz" in names
        assert len(names) >= 30

    def test_gm_instruments_extended(self):
        assert len(GM_INSTRUMENTS_EXTENDED) >= 100
        # Uses lowercase keys
        assert "piano" in GM_INSTRUMENTS_EXTENDED
        assert "sitar" in GM_INSTRUMENTS_EXTENDED

    def test_get_genre_instruments_pop(self):
        instruments = get_genre_instruments("pop")
        assert isinstance(instruments, list)
        assert len(instruments) >= 3

    def test_get_genre_instruments_subgenre_inherits(self):
        """Sub-genre should have instruments (either own or inherited)."""
        root_instruments = get_genre_instruments("jazz")
        sub_instruments = get_genre_instruments("jazz.bebop")
        assert len(root_instruments) > 0
        assert len(sub_instruments) > 0


# =====================================================================
# SECTION 4: Backward Compatibility Tests
# =====================================================================


class TestBackwardCompatibility:
    """Ensure the original 10 genre IDs still work."""

    @pytest.mark.parametrize("genre_id", [
        "pop", "rock", "electronic", "hiphop", "jazz",
        "blues", "classical", "lofi", "ambient", "cinematic",
    ])
    def test_original_genres_exist(self, genre_id):
        node = get_genre(genre_id)
        assert node is not None
        assert node.id == genre_id

    def test_funk_alias_works(self):
        node = find_by_alias("funk")
        assert node is not None
        assert "funk" in node.id


# =====================================================================
# SECTION 5: Integration with constants.py
# =====================================================================


class TestConstantsIntegration:
    """Verify that constants.py correctly imports from the registry."""

    def test_genre_config_populated(self):
        from src.app.constants import GENRE_CONFIG
        assert len(GENRE_CONFIG) > 10
        assert "pop" in GENRE_CONFIG
        for genre, cfg in GENRE_CONFIG.items():
            assert "tempo_range" in cfg
            assert "mode" in cfg  # default_scale mapped to 'mode'

    def test_scales_match_registry(self):
        from src.app.constants import SCALES
        assert SCALES is SCALES_EXTENDED

    def test_gm_instruments_match_registry(self):
        from src.app.constants import GM_INSTRUMENTS
        assert GM_INSTRUMENTS is GM_INSTRUMENTS_EXTENDED

    def test_chord_progressions_cover_root_genres(self):
        from src.app.constants import CHORD_PROGRESSIONS
        for root in ["pop", "rock", "jazz", "blues", "electronic", "classical"]:
            assert root in CHORD_PROGRESSIONS, f"Missing chord progressions for '{root}'"


# =====================================================================
# SECTION 6: Schema Integration Tests
# =====================================================================


class TestSchemaIntegration:
    """Verify that schema.py correctly uses the registry."""

    def test_all_root_genres_in_supported(self):
        from src.intent.schema import SUPPORTED_GENRES
        for gid in ["pop", "rock", "jazz", "blues", "electronic", "ambient"]:
            assert gid in SUPPORTED_GENRES

    def test_world_genres_in_supported(self):
        from src.intent.schema import SUPPORTED_GENRES
        for gid in ["jazz.bossa_nova", "african.afrobeat", "asian.bollywood"]:
            assert gid in SUPPORTED_GENRES

    def test_supported_scales_includes_world(self):
        from src.intent.schema import SUPPORTED_SCALES
        assert "hijaz" in SUPPORTED_SCALES
        assert "phrygian_dominant" in SUPPORTED_SCALES

    def test_genre_alias_resolution_in_schema(self):
        from src.intent.schema import ParsedIntent
        intent = ParsedIntent.model_validate({
            "genre": {"primary": "bossa nova", "confidence": 0.9},
        })
        assert "bossa" in intent.genre.primary.lower()

    def test_subgenre_direct_in_schema(self):
        from src.intent.schema import ParsedIntent
        intent = ParsedIntent.model_validate({
            "genre": {"primary": "electronic.house", "confidence": 0.9},
        })
        assert intent.genre.primary == "electronic.house"


# =====================================================================
# SECTION 7: Genre Validator Integration
# =====================================================================


class TestGenreValidatorIntegration:
    """Verify the genre validator uses registry data."""

    def test_validator_has_world_genres(self):
        from src.analysis.genre_validator import GenreCharacteristic
        genres = GenreCharacteristic.GENRES
        # Should have more than the original 9
        assert len(genres) > 15
        # Should include world genres
        for g in ["latin", "african", "asian"]:
            assert g in genres, f"Validator missing genre '{g}'"
