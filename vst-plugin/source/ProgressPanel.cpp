/*
  ==============================================================================
    ProgressPanel.cpp
    text2midi VST3 Plugin — Generation progress display implementation
  ==============================================================================
*/

#include "ProgressPanel.h"
#include "PluginConfig.h"

//==============================================================================
ProgressPanel::ProgressPanel()
{
    statusLabel.setFont (juce::Font (juce::FontOptions (14.0f)));
    statusLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColSubtext));
    statusLabel.setJustificationType (juce::Justification::centredLeft);
    addAndMakeVisible (statusLabel);

    setVisible (false);
}

//==============================================================================
void ProgressPanel::paint (juce::Graphics& g)
{
    auto bounds = getLocalBounds().toFloat();

    g.setColour (juce::Colour (text2midi::kColSurface0));
    g.fillRoundedRectangle (bounds, 6.0f);

    // Progress bar background
    auto barArea = bounds.reduced (10).removeFromBottom (6);
    g.setColour (juce::Colour (text2midi::kColSurface1));
    g.fillRoundedRectangle (barArea, 3.0f);

    // Progress bar fill
    if (currentNode > 0)
    {
        float progress = juce::jlimit (0.0f, 1.0f,
            static_cast<float> (currentNode) / static_cast<float> (kTotalNodes));
        auto fillArea = barArea.withWidth (barArea.getWidth() * progress);
        g.setColour (juce::Colour (text2midi::kColBlue));
        g.fillRoundedRectangle (fillArea, 3.0f);
    }
}

void ProgressPanel::resized()
{
    auto area = getLocalBounds().reduced (10);
    statusLabel.setBounds (area.removeFromTop (area.getHeight() - 16));
}

//==============================================================================
void ProgressPanel::show()
{
    currentNode = 0;
    statusLabel.setText ("Starting generation...", juce::dontSendNotification);
    statusLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColSubtext));
    setVisible (true);
    repaint();
}

void ProgressPanel::hide()
{
    setVisible (false);
}

void ProgressPanel::updateProgress (int nodeIndex, const juce::String& nodeName)
{
    currentNode = nodeIndex;
    auto text = juce::String ("Step ") + juce::String (nodeIndex) + "/"
              + juce::String (kTotalNodes) + ": " + nodeName + "...";
    statusLabel.setText (text, juce::dontSendNotification);
    statusLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColText));
    repaint();
}

void ProgressPanel::markComplete (float qualityScore)
{
    currentNode = kTotalNodes;

    auto scoreStr = juce::String (qualityScore, 2);
    statusLabel.setText (juce::String (juce::CharPointer_UTF8 ("\xe2\x9c\x93 Complete \xe2\x80\x94 Quality: "))
                         + scoreStr + "/1.0",
                         juce::dontSendNotification);
    statusLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColGreen));
    repaint();
}

void ProgressPanel::markError (const juce::String& message)
{
    statusLabel.setText (juce::String (juce::CharPointer_UTF8 ("\xe2\x9c\x97 Error: ")) + message,
                         juce::dontSendNotification);
    statusLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColRed));
    repaint();
}
