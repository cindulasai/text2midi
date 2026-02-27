/*
  ==============================================================================
    OutputPanel.cpp
    text2midi VST3 Plugin — Generation results display implementation
  ==============================================================================
*/

#include "OutputPanel.h"
#include "PluginConfig.h"

//==============================================================================
OutputPanel::OutputPanel()
{
    summaryLabel.setFont (juce::Font (juce::FontOptions (13.0f)));
    summaryLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColSubtext));
    summaryLabel.setJustificationType (juce::Justification::centredLeft);
    addAndMakeVisible (summaryLabel);

    trackList.setModel (this);
    trackList.setRowHeight (22);
    trackList.setColour (juce::ListBox::backgroundColourId, juce::Colour (text2midi::kColSurface1));
    trackList.setColour (juce::ListBox::outlineColourId, juce::Colours::transparentBlack);
    addAndMakeVisible (trackList);

    addAndMakeVisible (draggable);

    changeKeyButton.setColour (juce::TextButton::buttonColourId, juce::Colours::transparentBlack);
    changeKeyButton.setColour (juce::TextButton::textColourOffId, juce::Colour (text2midi::kColSubtext));
    changeKeyButton.addListener (this);
    addAndMakeVisible (changeKeyButton);

    setVisible (false);
}

//==============================================================================
void OutputPanel::paint (juce::Graphics& g)
{
    g.setColour (juce::Colour (text2midi::kColSurface0));
    g.fillRoundedRectangle (getLocalBounds().toFloat(), 6.0f);
}

void OutputPanel::resized()
{
    auto area = getLocalBounds().reduced (10);

    summaryLabel.setBounds (area.removeFromTop (24));
    area.removeFromTop (4);

    changeKeyButton.setBounds (area.removeFromBottom (24));
    area.removeFromBottom (4);

    draggable.setBounds (area.removeFromBottom (64));
    area.removeFromBottom (4);

    trackList.setBounds (area);
}

//==============================================================================
void OutputPanel::buttonClicked (juce::Button* button)
{
    if (button == &changeKeyButton && listener != nullptr)
        listener->changeApiKeyRequested();
}

//==============================================================================
void OutputPanel::setResult (const juce::var& result)
{
    tracks.clear();

    // Parse tracks array
    auto tracksVar = result.getProperty ("tracks", juce::var());
    if (auto* arr = tracksVar.getArray())
    {
        for (const auto& t : *arr)
        {
            TrackRow row;
            row.channel    = static_cast<int> (t.getProperty ("channel", 0));
            row.instrument = t.getProperty ("instrument", "unknown").toString();
            row.noteCount  = static_cast<int> (t.getProperty ("note_count", 0));
            tracks.add (row);
        }
    }

    // Summary text
    auto genre = result.getProperty ("genre", "").toString();
    auto tempo = static_cast<int> (result.getProperty ("tempo", 120));
    auto numTracks = tracks.size();

    auto summary = juce::String (numTracks) + " tracks | " + genre
                 + " | " + juce::String (tempo) + " BPM";
    summaryLabel.setText (summary, juce::dontSendNotification);

    // Draggable MIDI
    auto midiPath = result.getProperty ("midi_path", "").toString();
    if (midiPath.isNotEmpty())
    {
        auto file = juce::File (midiPath);
        draggable.setMidiFile (midiPath, file.getFileName(), summary);
    }

    trackList.updateContent();
    setVisible (true);
}

void OutputPanel::clear()
{
    tracks.clear();
    summaryLabel.setText ("", juce::dontSendNotification);
    draggable.clear();
    trackList.updateContent();
    setVisible (false);
}

//==============================================================================
// ListBoxModel
//==============================================================================

int OutputPanel::getNumRows()
{
    return tracks.size();
}

void OutputPanel::paintListBoxItem (int row, juce::Graphics& g,
                                     int width, int height, bool rowIsSelected)
{
    if (! juce::isPositiveAndBelow (row, tracks.size()))
        return;

    auto bgCol = rowIsSelected ? juce::Colour (text2midi::kColSurface2)
                               : juce::Colour (text2midi::kColSurface1);
    g.fillAll (bgCol);

    const auto& track = tracks.getReference (row);

    auto text = "Ch " + juce::String (track.channel) + ": "
              + track.instrument + " (" + juce::String (track.noteCount) + " notes)";

    g.setColour (juce::Colour (text2midi::kColText));
    g.setFont (juce::Font (juce::FontOptions (12.0f)));
    g.drawText (text, 8, 0, width - 16, height, juce::Justification::centredLeft);
}
