/*
  ==============================================================================
    DraggableMidiFile.h
    text2midi VST3 Plugin — Drag-and-drop MIDI file component
  ==============================================================================
*/

#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

class DraggableMidiFile : public juce::Component,
                          public juce::SettableTooltipClient
{
public:
    DraggableMidiFile();

    void paint (juce::Graphics& g) override;
    void resized() override {}

    void mouseDrag (const juce::MouseEvent& event) override;
    void mouseUp (const juce::MouseEvent& event) override;

    /** Set the MIDI file path (enables drag). */
    void setMidiFile (const juce::String& path, const juce::String& displayName,
                      const juce::String& durationText);

    /** Clear the current file (disables drag). */
    void clear();

    bool hasFile() const { return midiFilePath.isNotEmpty(); }

private:
    juce::String midiFilePath;
    juce::String fileName;
    juce::String duration;
    bool isDragging = false;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (DraggableMidiFile)
};
