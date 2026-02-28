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
    // Title
    titleLabel.setText (juce::CharPointer_UTF8 ("\xe2\x9c\xa8 Generation Results"), juce::dontSendNotification);
    titleLabel.setFont (juce::Font (juce::FontOptions (14.0f).withStyle ("Bold")));
    titleLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColText));
    addAndMakeVisible (titleLabel);

    // Quality score badge
    qualityLabel.setFont (juce::Font (juce::FontOptions (13.0f).withStyle ("Bold")));
    qualityLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColGreen));
    qualityLabel.setJustificationType (juce::Justification::centredRight);
    addAndMakeVisible (qualityLabel);

    // Summary
    summaryLabel.setFont (juce::Font (juce::FontOptions (12.0f)));
    summaryLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColSubtext));
    summaryLabel.setJustificationType (juce::Justification::centredLeft);
    addAndMakeVisible (summaryLabel);

    // MIDI file path
    midiPathLabel.setFont (juce::Font (juce::FontOptions (10.0f)));
    midiPathLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColOverlay0));
    midiPathLabel.setJustificationType (juce::Justification::centredLeft);
    addAndMakeVisible (midiPathLabel);

    // Track list
    trackList.setModel (this);
    trackList.setRowHeight (24);
    trackList.setColour (juce::ListBox::backgroundColourId, juce::Colour (text2midi::kColSurface1));
    trackList.setColour (juce::ListBox::outlineColourId, juce::Colours::transparentBlack);
    addAndMakeVisible (trackList);

    addAndMakeVisible (draggable);

    // Open folder button
    openFolderButton.setColour (juce::TextButton::buttonColourId, juce::Colour (text2midi::kColSurface1));
    openFolderButton.setColour (juce::TextButton::textColourOffId, juce::Colour (text2midi::kColBlue));
    openFolderButton.addListener (this);
    addAndMakeVisible (openFolderButton);

    // Settings button
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

    // Title row with quality badge
    auto titleRow = area.removeFromTop (22);
    titleLabel.setBounds (titleRow.removeFromLeft (titleRow.getWidth() / 2));
    qualityLabel.setBounds (titleRow);
    area.removeFromTop (2);

    // Summary
    summaryLabel.setBounds (area.removeFromTop (18));
    area.removeFromTop (2);

    // MIDI path
    midiPathLabel.setBounds (area.removeFromTop (14));
    area.removeFromTop (4);

    // Bottom row: buttons
    auto bottomRow = area.removeFromBottom (26);
    changeKeyButton.setBounds (bottomRow.removeFromRight (70));
    openFolderButton.setBounds (bottomRow.removeFromRight (90));
    area.removeFromBottom (4);

    // Draggable MIDI
    draggable.setBounds (area.removeFromBottom (64));
    area.removeFromBottom (4);

    // Track list fills remaining
    trackList.setBounds (area);
}

//==============================================================================
void OutputPanel::buttonClicked (juce::Button* button)
{
    if (button == &changeKeyButton && listener != nullptr)
        listener->changeApiKeyRequested();

    if (button == &openFolderButton && lastMidiPath.isNotEmpty())
    {
        auto file = juce::File (lastMidiPath);
        if (file.existsAsFile())
            file.getParentDirectory().startAsProcess();
        else
            juce::File::getSpecialLocation (juce::File::userDesktopDirectory)
                .getChildFile ("..").startAsProcess();
    }
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
            row.trackType  = t.getProperty ("track_type", "").toString();
            tracks.add (row);
        }
    }

    // Quality score
    auto quality = static_cast<float> (result.getProperty ("quality_score", 0.0));
    auto qualityStr = juce::String (quality, 2) + " / 1.0";
    if (quality >= 0.8f)
    {
        qualityLabel.setText (juce::CharPointer_UTF8 ("\xe2\xad\x90 ") + qualityStr, juce::dontSendNotification);
        qualityLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColGreen));
    }
    else if (quality >= 0.5f)
    {
        qualityLabel.setText (qualityStr, juce::dontSendNotification);
        qualityLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColYellow));
    }
    else
    {
        qualityLabel.setText (qualityStr, juce::dontSendNotification);
        qualityLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColPeach));
    }

    // Summary text
    auto genre = result.getProperty ("genre", "").toString();
    auto tempo = static_cast<int> (result.getProperty ("tempo", 120));
    auto numTracks = tracks.size();

    auto summary = juce::String (numTracks) + " tracks  |  "
                 + (genre.isNotEmpty() ? genre + "  |  " : "")
                 + juce::String (tempo) + " BPM";
    summaryLabel.setText (summary, juce::dontSendNotification);

    // MIDI path
    auto midiPath = result.getProperty ("midi_path", "").toString();
    lastMidiPath = midiPath;
    if (midiPath.isNotEmpty())
    {
        auto file = juce::File (midiPath);
        midiPathLabel.setText (file.getFileName(), juce::dontSendNotification);
        draggable.setMidiFile (midiPath, file.getFileName(), summary);
    }

    trackList.updateContent();
    setVisible (true);
}

void OutputPanel::clear()
{
    tracks.clear();
    summaryLabel.setText ("", juce::dontSendNotification);
    qualityLabel.setText ("", juce::dontSendNotification);
    midiPathLabel.setText ("", juce::dontSendNotification);
    lastMidiPath = {};
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

    // Channel badge
    auto chText = "Ch " + juce::String (track.channel);
    g.setColour (juce::Colour (text2midi::kColBlue));
    g.setFont (juce::Font (juce::FontOptions (11.0f).withStyle ("Bold")));
    g.drawText (chText, 8, 0, 40, height, juce::Justification::centredLeft);

    // Instrument name
    g.setColour (juce::Colour (text2midi::kColText));
    g.setFont (juce::Font (juce::FontOptions (12.0f)));
    g.drawText (track.instrument, 52, 0, width - 160, height, juce::Justification::centredLeft, true);

    // Note count + track type (right-aligned)
    auto rightText = juce::String (track.noteCount) + " notes";
    if (track.trackType.isNotEmpty())
        rightText += " (" + track.trackType + ")";
    g.setColour (juce::Colour (text2midi::kColSubtext));
    g.setFont (juce::Font (juce::FontOptions (11.0f)));
    g.drawText (rightText, width - 140, 0, 132, height, juce::Justification::centredRight);
}
