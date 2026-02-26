# -*- coding: utf-8 -*-
"""
Educational Insights Engine: Music theory explanations and learning content
USP Feature #5: Learn while you create
Generates educational content explaining the music theory used in compositions
"""

from dataclasses import dataclass
from typing import List, Dict
from enum import Enum


class MusicTheoryConcept(Enum):
    """Music theory concepts explained in compositions."""
    INTERVALS = "intervals"
    CHORDS = "chords"
    SCALES = "scales"
    CADENCES = "cadences"
    VOICE_LEADING = "voice_leading"
    MODULATION = "modulation"
    RHYTHM = "rhythm"
    DYNAMICS = "dynamics"
    ORCHESTRATION = "orchestration"
    MELODY = "melody"
    HARMONY = "harmony"
    FORM = "form"


@dataclass
class EducationalExplanation:
    """Educational content about music theory used in composition."""
    concept: MusicTheoryConcept
    title: str
    explanation: str  # Plain English explanation
    example_from_composition: str  # How it's used in this specific piece
    why_it_matters: str  # Musical impact
    further_learning: List[str] = None
    difficulty_level: str = "intermediate"  # beginner, intermediate, advanced


class EducationalInsightsEngine:
    """
    Generates musictheory educational content based on compositions.
    Helps users learn while creating music.
    """
    
    CONCEPT_EXPLANATIONS = {
        MusicTheoryConcept.INTERVALS: {
            "title": "Understanding Intervals",
            "explanation": """Intervals are the distance between two notes measured in semitones (half-steps). 
            Unison (0), Minor 2nd (1), Major 2nd (2), Minor 3rd (3), Major 3rd (4), Perfect 4th (5), 
            Tritone (6), Perfect 5th (7), Minor 6th (8), Major 6th (9), Minor 7th (10), Major 7th (11), Octave (12).
            
            Consonant intervals (pleasant): Perfect 4th, 5th, octave; Major/minor 3rds, 6ths
            Dissonant intervals (tense): Tritone, seconds, sevenths""",
            "why_it_matters": "Intervals determine consonance/dissonance creating tension and resolution"
        },
        MusicTheoryConcept.CHORDS: {
            "title": "Building Chords",
            "explanation": """Chords are built by stacking notes. Triads use 3 notes (root, 3rd, 5th).
            - Major triad: root + major 3rd + perfect 5th = bright, happy sound
            - Minor triad: root + minor 3rd + perfect 5th = dark, sad sound
            - Diminished: root + minor 3rd + diminished 5th = tense, unstable
            - Augmented: root + major 3rd + augmented 5th = ambiguous, suspended
            
            Extensions add color: 7ths (dominant, major, minor), 9ths, 11ths, 13ths""",
            "why_it_matters": "Chords provide harmonic foundation and emotional color"
        },
        MusicTheoryConcept.SCALES: {
            "title": "Scales: Musical Alphabets",
            "explanation": """Scales are ordered collections of notes within an octave.
            
            Major scale: Whole-Whole-Half-Whole-Whole-Whole-Half pattern from root
            - Bright, happy, definitive sound
            
            Natural Minor: Whole-Half-Whole-Whole-Half-Whole-Whole pattern
            - Dark, sad, introspective sound
            
            Pentatonic (5-note): Removes 4th and 7th degrees
            - Simple, universal, very musical
            
            Blues scale: Add flat-5 to minor pentatonic
            - Soulful, expressive, bent notes""",
            "why_it_matters": "Scale choice fundamentally determines the tonal character of music"
        },
        MusicTheoryConcept.CADENCES: {
            "title": "Cadences: Musical Punctuation",
            "explanation": """Cadences are chord progressions that provide closure or transition.
            
            Strong resolutions:
            - Perfect cadence (V→I): Most conclusive, ends phrases definitively
            - Plagal cadence (IV→I): "Amen cadence", warm, traditional
            
            Weaker resolutions:
            - Half cadence (→V): Poses question, creates expectation
            - Deceptive cadence (V→vi): Subverts expectation, continues forward
            
            Common progression: I-IV-V-I creates natural harmonic flow""",
            "why_it_matters": "Cadences create satisfying harmonic structures and narrative arc"
        },
        MusicTheoryConcept.MELODY: {
            "title": "Crafting Memorable Melodies",
            "explanation": """Strong melodies have:
            
            - Clear contour: Rise and fall creating interest (not just static)
            - Singability: Comfortable intervals, mostly stepwise motion
            - Repetition with variation: Return to recognizable themes with changes
            - Climax: A peak note or phrase that stands out
            - Clear phrasing: Question/answer structure (antecedent/consequent)
            
            Bad melodies: Too random, too repetitive, uncomfortable intervals, no shape""",
            "why_it_matters": "A strong melody is what listeners remember and enjoy"
        },
        MusicTheoryConcept.HARMONY: {
            "title": "Harmonic Movement and Voice Leading",
            "explanation": """Harmony moves through space creating relationship and tension.
            
            Rules of voice leading (minimize awkwardness):
            - Avoid parallel perfects (5ths, octaves between melody and bass)
            - Contrary motion (voices move in opposite directions) is ideal
            - Common tone connection (chords share a note requiring less movement)
            - Smooth voice leading = professional sound
            
            Functional harmony: Chords have roles (tonic=home, subdominant=moving, dominant=resolving)""",
            "why_it_matters": "Good voice leading creates smooth, professional harmonic movement"
        },
        MusicTheoryConcept.RHYTHM: {
            "title": "Rhythm and Meter Fundamentals",
            "explanation": """Rhythm is the pattern of sounds and silences.
            
            - Meter organizes beats: 4/4 (4 beats per bar, quarter note gets beat)
            - Syncopation: Emphasis on unexpected beats creates interest
            - Note values: Whole (4 beats), Half (2), Quarter (1), Eighth (1/2), Sixteenth (1/4)
            - Rest: Silence is as important as sound for groove
            
            Good rhythm creates groove, Bad rhythm sounds stiff or confusing""",
            "why_it_matters": "Rhythm creates movement, groove, and propels the music forward"
        },
        MusicTheoryConcept.ORCHESTRATION: {
            "title": "Orchestration: Instrument Choice and Arrangement",
            "explanation": """Different instruments have different characters:
            - Strings: Warm, blended, expressive
            - Woodwinds: Bright, agile, lyrical
            - Brass: Bold, heroic, powerful, darker when soft
            - Percussion: Rhythmic, textural, dramatic
            - Keyboards: Versatile, precise, omnipresent
            
            Orchestration principles:
            - Doubling (multiple instruments) = fuller, richer sound
            - Layers (high-mid-low) = balance and clarity
            - Solo vs. ensemble = contrast and focus""",
            "why_it_matters": "Orchestration creates the sonic character listeners hear"
        },
        MusicTheoryConcept.DYNAMICS: {
            "title": "Dynamics: Sound Intensity and Expression",
            "explanation": """Dynamics are volume and intensity variations.
            
            Markings: ppp (very soft) → pp → p → mp → mf → f → ff → fff (very loud)
            
            Functions:
            - Emphasis: Make important moments stand out
            - Contrast: Move between sections with different intensities
            - Expression: Match emotional arc of the piece
            - Realism: Natural music has dynamic variation
            
            A piece without dynamics = monotonous. With careful dynamics = moving, expressive.""",
            "why_it_matters": "Dynamics create expression and emotional impact"
        },
        MusicTheoryConcept.FORM: {
            "title": "Musical Form and Structure",
            "explanation": """Form describes how a piece is organized.
            
            - Binary (AB): Two contrasting sections
            - Ternary (ABA): Third section returns to first idea
            - Rondo (ABACA): Opening returns repeatedly between new sections
            - Sonata (exp-dev-recap): Present, develop, restate ideas
            - Theme and Variations: One idea modified repeatedly
            
            Standard pop form: Intro-Verse-Chorus-Verse-Chorus-Bridge-Chorus-Outro""",
            "why_it_matters": "Form creates coherent narrative and listener expectation"
        }
    }
    
    @staticmethod
    def generate_educational_content(
        concepts_used: List[MusicTheoryConcept],
        composition_analysis: Dict
    ) -> List[EducationalExplanation]:
        """
        Generate educational content for concepts used in the composition.
        """
        explanations = []
        
        for concept in concepts_used:
            if concept not in EducationalInsightsEngine.CONCEPT_EXPLANATIONS:
                continue
            
            concept_data = EducationalInsightsEngine.CONCEPT_EXPLANATIONS[concept]
            
            # Create explanation with composition-specific examples
            explanation = EducationalExplanation(
                concept=concept,
                title=concept_data["title"],
                explanation=concept_data["explanation"],
                example_from_composition=EducationalInsightsEngine._generate_example(
                    concept, composition_analysis
                ),
                why_it_matters=concept_data["why_it_matters"],
                further_learning=EducationalInsightsEngine._get_learning_resources(concept)
            )
            
            explanations.append(explanation)
        
        return explanations
    
    @staticmethod
    def _generate_example(concept: MusicTheoryConcept, analysis: Dict) -> str:
        """Generate specific example from the analyzed composition."""
        
        examples = {
            MusicTheoryConcept.INTERVALS: f"""
            In your {analysis.get('genre', 'composition')}, the main melody uses:
            - Major 3rds in the rising phrase (pleasant, bright intervals)
            - Perfect 5ths in the harmonic foundation (stable, resolving)
            - This mix creates interest while maintaining consonance""",
            
            MusicTheoryConcept.CHORDS: f"""
            Your composition uses these chord qualities:
            - {analysis.get('chord_types', 'mostly major and minor triads')}
            - The progression {analysis.get('progression', 'I-IV-V-I')} creates strong harmonic movement
            - This returns to home (I) giving sense of completion""",
            
            MusicTheoryConcept.SCALES: f"""
            Your {analysis.get('genre')} uses the {analysis.get('scale', 'major scale')}:
            - Scale degree patterns create the characteristic {analysis.get('mood', 'mood')} sound
            - The focus on certain scale degrees (3rd, 5th, 7th) defines the tonal center""",
            
            MusicTheoryConcept.MELODY: f"""
            Your melody demonstrates:
            - Clear contour with rises and falls (not monotone)
            - Range of {analysis.get('range', '2 octaves')} for interest without extremes
            - Repetition of core motif with small variations for memorability""",
            
            MusicTheoryConcept.RHYTHM: f"""
            The rhythm pattern in your {analysis.get('genre')} demonstrates:
            - Clear meter of {analysis.get('time_sig', '4/4')} establishing foundation
            - {analysis.get('rhythm_char', 'Steady pulse with occasional syncopation')} for groove
            - Mix of note values (mostly quarters/eighths) for clarity""",
            
            MusicTheoryConcept.ORCHESTRATION: f"""
            Your orchestration includes:
            - {analysis.get('melody_instr', 'Melodic instrument')} leading the harmonic idea
            - {analysis.get('support_instr', 'Supporting instruments')} providing harmonic foundation
            - This creates clear hierarchy and listener focus""",
            
            MusicTheoryConcept.DYNAMICS: f"""
            The dynamics in your piece:
            - Begin at {analysis.get('start_dynamic', 'moderate')} intensity
            - Build toward the middle/climax for tension
            - Return to {analysis.get('end_dynamic', 'softer')} for closure
            - This arc engages listeners emotionally""",
        }
        
        return examples.get(concept, f"This composition uses {concept.value} effectively")
    
    @staticmethod
    def _get_learning_resources(concept: MusicTheoryConcept) -> List[str]:
        """Get further learning resources for concept."""
        
        resources = {
            MusicTheoryConcept.INTERVALS: [
                "Practice singing intervals: Start with octaves/5ths, add smaller intervals",
                "Transcribe melodies to ear-train interval recognition",
                "Study interval quality categories (consonant vs. dissonant)"
            ],
            MusicTheoryConcept.CHORDS: [
                "Learn chord construction: root position, 1st inversion, 2nd inversion",
                "Explore extended chords: 7ths, 9ths, 11ths, 13ths",
                "Study chord progressions in songs you love"
            ],
            MusicTheoryConcept.SCALES: [
                "Practice scales daily: all 12 major keys, all 12 minor keys",
                "Compare major vs minor vs pentatonic sound",
                "Explore modes: Ionian, Dorian, Phrygian, etc."
            ],
            MusicTheoryConcept.MELODY: [
                "Analyze melodies from master composers",
                "Identify phrase structure (4/8/16 bar patterns)",
                "Transcribe and sing melodies for internalization"
            ],
            MusicTheoryConcept.RHYTHM: [
                "Study different time signatures and meters",
                "Practice syncopation exercises",
                "Listen to polyrhythmic music for advanced understanding"
            ],
            MusicTheoryConcept.HARMONY: [
                "Study voice leading rules with 4-part writing",
                "Analyze Bach chorales for perfect voice leading",
                "Compose progressions with smooth voice movement"
            ]
        }
        
        return resources.get(concept, ["Further study recommended"])
    
    @staticmethod
    def create_learning_guide(
        composition_genre: str,
        used_concepts: List[MusicTheoryConcept],
        difficulty: str = "intermediate"
    ) -> str:
        """Create a comprehensive learning guide for the composition."""
        
        guide = f"""# Music Theory Learning Guide
        
## Composition: {composition_genre.capitalize()} Piece

This composition teaches the following music theory concepts:

"""
        
        for concept in used_concepts:
            if concept in EducationalInsightsEngine.CONCEPT_EXPLANATIONS:
                data = EducationalInsightsEngine.CONCEPT_EXPLANATIONS[concept]
                guide += f"\n### {data['title']}\n\n"
                guide += f"{data['explanation']}\n\n"
                guide += f"**Why this matters:** {data['why_it_matters']}\n\n"
        
        guide += """
## Practice Suggestions

1. **Active Listening**: Listen to the composition focusing on each concept
2. **Singing**: Sing melodies and main harmonic movements
3. **Analysis**: Write down the chord changes and structure
4. **Application**: Create your own short piece using these same concepts
5. **Comparison**: Compare with other songs in the same genre

## Key Takeaways

- Understanding these concepts helps you become a more deliberate musician
- Professional musicians apply these principles instinctively
- The more you study, the better your creative instincts become
"""
        
        return guide
