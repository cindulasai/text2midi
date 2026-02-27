/*
  ==============================================================================
    ProgressPanel.h
    text2midi VST3 Plugin — Generation progress display
  ==============================================================================
*/

#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

class ProgressPanel : public juce::Component
{
public:
    ProgressPanel();

    void resized() override;
    void paint (juce::Graphics& g) override;

    /** Show the panel and reset progress. */
    void show();

    /** Hide the panel. */
    void hide();

    /** Update progress with current node info. */
    void updateProgress (int nodeIndex, const juce::String& nodeName);

    /** Mark generation as complete. */
    void markComplete (float qualityScore);

    /** Mark generation as failed. */
    void markError (const juce::String& message);

private:
    juce::Label statusLabel;
    int currentNode = 0;
    static constexpr int kTotalNodes = 8;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (ProgressPanel)
};
