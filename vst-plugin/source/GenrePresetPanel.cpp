/*
  ==============================================================================
    GenrePresetPanel.cpp
    text2midi VST3 Plugin — Genre presets + Surprise Me implementation
  ==============================================================================
*/

#include "GenrePresetPanel.h"
#include "PluginConfig.h"

//==============================================================================
GenrePresetPanel::GenrePresetPanel()
{
    buildGenres();

    titleLabel.setText ("Quick Presets", juce::dontSendNotification);
    titleLabel.setFont (juce::Font (juce::FontOptions (12.0f).withStyle ("Bold")));
    titleLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColSubtext));
    addAndMakeVisible (titleLabel);

    // Surprise button
    surpriseButton.setColour (juce::TextButton::buttonColourId, juce::Colour (text2midi::kColPeach));
    surpriseButton.setColour (juce::TextButton::textColourOnId, juce::Colour (text2midi::kColBase));
    surpriseButton.setColour (juce::TextButton::textColourOffId, juce::Colour (text2midi::kColBase));
    surpriseButton.addListener (this);
    addAndMakeVisible (surpriseButton);

    // Create genre chip buttons
    for (const auto& g : genres)
    {
        auto* btn = new juce::TextButton (g.label);
        btn->setColour (juce::TextButton::buttonColourId, juce::Colour (text2midi::kColSurface1));
        btn->setColour (juce::TextButton::textColourOnId, juce::Colour (text2midi::kColText));
        btn->setColour (juce::TextButton::textColourOffId, juce::Colour (text2midi::kColText));
        btn->addListener (this);
        addAndMakeVisible (btn);
        genreButtons.add (btn);
    }
}

//==============================================================================
void GenrePresetPanel::paint (juce::Graphics& g)
{
    g.setColour (juce::Colour (text2midi::kColSurface0));
    g.fillRoundedRectangle (getLocalBounds().toFloat(), 6.0f);
}

void GenrePresetPanel::resized()
{
    auto area = getLocalBounds().reduced (8);

    // Title row with surprise button
    auto titleRow = area.removeFromTop (26);
    titleLabel.setBounds (titleRow.removeFromLeft (100));
    surpriseButton.setBounds (titleRow.removeFromRight (titleRow.getWidth()));

    area.removeFromTop (4);

    // Genre chips in rows - calculate chip layout
    const int chipHeight = 26;
    const int chipGap = 4;
    int x = area.getX();
    int y = area.getY();
    int maxWidth = area.getWidth();

    for (auto* btn : genreButtons)
    {
        int chipWidth = btn->getButtonText().length() * 8 + 20;
        chipWidth = juce::jmax (chipWidth, 60);

        if (x + chipWidth > area.getX() + maxWidth && x > area.getX())
        {
            x = area.getX();
            y += chipHeight + chipGap;
        }

        btn->setBounds (x, y, chipWidth, chipHeight);
        x += chipWidth + chipGap;
    }
}

//==============================================================================
void GenrePresetPanel::buttonClicked (juce::Button* button)
{
    if (listener == nullptr)
        return;

    if (button == &surpriseButton)
    {
        listener->genrePresetSelected (getRandomSurprise());
        return;
    }

    for (int i = 0; i < genreButtons.size(); ++i)
    {
        if (genreButtons[i] == button)
        {
            listener->genrePresetSelected (genres[i].prompt);
            return;
        }
    }
}

//==============================================================================
void GenrePresetPanel::buildGenres()
{
    genres.add ({ "Ambient",     "dreamy ambient soundscape with ethereal pads and soft textures" });
    genres.add ({ "Jazz",        "smooth jazz with piano, upright bass, and brushed drums" });
    genres.add ({ "Cinematic",   "epic cinematic orchestral score with strings, brass, and percussion" });
    genres.add ({ "Lo-Fi",       "chill lo-fi hip-hop beat with warm keys and vinyl crackle" });
    genres.add ({ "Electronic",  "energetic electronic track with synthesizers and heavy bass" });
    genres.add ({ "Classical",   "elegant classical piano sonata in a romantic style" });
    genres.add ({ "Funk",        "groovy funk with slap bass, clavinet, and tight drums" });
    genres.add ({ "Pop",         "catchy pop song with bright synths, piano, and punchy drums" });
    genres.add ({ "Rock",        "hard-hitting rock with electric guitar, bass, and powerful drums" });
    genres.add ({ "Hip-Hop",     "boom bap hip-hop beat with sampled drums and deep bass" });
    genres.add ({ "R&B",         "smooth R&B with rhodes piano, bass, and mellow drums" });
    genres.add ({ "Latin",       "upbeat Latin track with congas, timbales, and rhythmic guitar" });
}

juce::String GenrePresetPanel::getRandomSurprise() const
{
    static const juce::StringArray surprises = {
        "a haunting midnight waltz played by a ghost orchestra in an abandoned cathedral",
        "funky disco groove with slap bass, wah guitar, and brass stabs at 118 BPM",
        "peaceful Japanese garden ambience with koto, shakuhachi flute, and soft rain",
        "aggressive trap beat with 808 bass, hi-hat rolls, and dark synth stabs",
        "whimsical circus theme with calliope organ, tubas, and snare drum",
        "melancholy piano ballad in D minor with cello countermelody and soft strings",
        "driving techno with pulsating bass, metallic percussion, and atmospheric pads",
        "upbeat bossa nova with nylon guitar, light percussion, and walking bass",
        "epic battle music with taiko drums, low brass, and choir",
        "lo-fi study beats with tape-warped Rhodes, vinyl crackle, and lazy drums",
        "dreamy shoegaze with layers of reverb-drenched guitars and ethereal vocals",
        "New Orleans second line groove with tuba, trumpet, trombone, and snare",
        "minimalist ambient with slowly evolving pad textures and sparse bell tones",
        "80s synthwave with arpeggiated synths, gated reverb drums, and neon bass",
        "West African highlife with palm wine guitar, talking drum, and shaker",
        "dark ambient horror soundtrack with dissonant drones and unsettling textures",
    };

    auto idx = juce::Random::getSystemRandom().nextInt (surprises.size());
    return surprises[idx];
}
