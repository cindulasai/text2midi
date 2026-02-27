/*
  ==============================================================================
    OutputPanel.h
    text2midi VST3 Plugin — Generation results display + draggable MIDI
  ==============================================================================
*/

#pragma once

#include "DraggableMidiFile.h"
#include <juce_gui_basics/juce_gui_basics.h>

class OutputPanel : public juce::Component,
                    public juce::ListBoxModel,
                    public juce::Button::Listener
{
public:
    OutputPanel();

    void resized() override;
    void paint (juce::Graphics& g) override;
    void buttonClicked (juce::Button* button) override;

    /** Populate the panel from a generation result (juce::var JSON). */
    void setResult (const juce::var& result);

    /** Clear the panel. */
    void clear();

    DraggableMidiFile& getDraggable() { return draggable; }

    // ── ListBoxModel ─────────────────────────────────────────────────────────
    int getNumRows() override;
    void paintListBoxItem (int row, juce::Graphics& g,
                           int width, int height, bool rowIsSelected) override;

    /** Listener for requesting API key change. */
    class Listener
    {
    public:
        virtual ~Listener() = default;
        virtual void changeApiKeyRequested() = 0;
    };

    void setListener (Listener* l) { listener = l; }

private:
    Listener* listener = nullptr;

    juce::Label          summaryLabel;
    juce::ListBox        trackList;
    DraggableMidiFile    draggable;
    juce::TextButton     changeKeyButton { "Change API Key" };

    // Track data
    struct TrackRow
    {
        int channel;
        juce::String instrument;
        int noteCount;
    };

    juce::Array<TrackRow> tracks;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (OutputPanel)
};
