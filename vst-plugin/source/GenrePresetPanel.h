/*
  ==============================================================================
    GenrePresetPanel.h
    text2midi VST3 Plugin — Genre presets + Surprise Me button
  ==============================================================================
*/

#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

class GenrePresetPanel : public juce::Component,
                         public juce::Button::Listener
{
public:
    GenrePresetPanel();

    void resized() override;
    void paint (juce::Graphics& g) override;
    void buttonClicked (juce::Button* button) override;

    /** Listener for preset / surprise selection. */
    class Listener
    {
    public:
        virtual ~Listener() = default;
        virtual void genrePresetSelected (const juce::String& prompt) = 0;
    };

    void setListener (Listener* l) { listener = l; }

private:
    Listener* listener = nullptr;

    juce::Label titleLabel;
    juce::TextButton surpriseButton { juce::CharPointer_UTF8 ("\xf0\x9f\x8e\xb2 Surprise Me") };

    // Genre chip buttons
    juce::OwnedArray<juce::TextButton> genreButtons;

    // Genre data: label → prompt template
    struct GenreEntry
    {
        juce::String label;
        juce::String prompt;
    };

    juce::Array<GenreEntry> genres;

    void buildGenres();
    juce::String getRandomSurprise() const;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (GenrePresetPanel)
};
