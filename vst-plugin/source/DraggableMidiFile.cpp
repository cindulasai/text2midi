/*
  ==============================================================================
    DraggableMidiFile.cpp
    text2midi VST3 Plugin — Drag-and-drop MIDI file component implementation
  ==============================================================================
*/

#include "DraggableMidiFile.h"
#include "PluginConfig.h"
#include <juce_gui_extra/juce_gui_extra.h>

//==============================================================================
DraggableMidiFile::DraggableMidiFile()
{
    setTooltip ("Drag this MIDI file to your DAW's arrangement view.\n"
                "Multi-channel MIDI will auto-create separate tracks.");
    setSize (200, 60);
}

//==============================================================================
void DraggableMidiFile::paint (juce::Graphics& g)
{
    auto bounds = getLocalBounds().toFloat().reduced (2.0f);

    // Gradient background (styled like a MIDI clip)
    juce::ColourGradient gradient (
        juce::Colour (text2midi::kColSurface1), bounds.getX(), bounds.getY(),
        juce::Colour (text2midi::kColSurface2), bounds.getRight(), bounds.getBottom(),
        false);
    g.setGradientFill (gradient);
    g.fillRoundedRectangle (bounds, 8.0f);

    // Border
    g.setColour (juce::Colour (text2midi::kColOverlay0));
    g.drawRoundedRectangle (bounds, 8.0f, 1.0f);

    if (! hasFile())
    {
        g.setColour (juce::Colour (text2midi::kColSubtext).withAlpha (0.5f));
        g.setFont (juce::Font (juce::FontOptions (12.0f)));
        g.drawText ("No MIDI file yet", bounds, juce::Justification::centred);
        return;
    }

    // Semi-transparent during drag
    float alpha = isDragging ? 0.5f : 1.0f;

    // MIDI icon (musical note symbol)
    g.setColour (juce::Colour (text2midi::kColBlue).withAlpha (alpha));
    g.setFont (juce::Font (juce::FontOptions (24.0f)));
    g.drawText (juce::CharPointer_UTF8 ("\xf0\x9f\x8e\xb5"), // 🎵
                bounds.removeFromLeft (40).toNearestInt(),
                juce::Justification::centred);

    // File name
    auto textArea = bounds.reduced (4, 0);
    g.setColour (juce::Colour (text2midi::kColText).withAlpha (alpha));
    g.setFont (juce::Font (juce::FontOptions (13.0f)));
    g.drawText (fileName, textArea.removeFromTop (textArea.getHeight() * 0.55f).toNearestInt(),
                juce::Justification::centredLeft, true);

    // Duration / info text
    g.setColour (juce::Colour (text2midi::kColSubtext).withAlpha (alpha));
    g.setFont (juce::Font (juce::FontOptions (11.0f)));
    g.drawText (duration, textArea.toNearestInt(),
                juce::Justification::centredLeft, true);
}

//==============================================================================
void DraggableMidiFile::mouseDrag (const juce::MouseEvent& /*event*/)
{
    if (! hasFile())
        return;

    auto* container = juce::DragAndDropContainer::findParentDragContainerFor (this);

    if (container != nullptr && ! container->isDragAndDropActive())
    {
        isDragging = true;
        repaint();

        juce::StringArray files;
        files.add (midiFilePath);
        container->performExternalDragDropOfFiles (files, true, this, nullptr);
    }
}

void DraggableMidiFile::mouseUp (const juce::MouseEvent& /*event*/)
{
    if (isDragging)
    {
        isDragging = false;
        repaint();
    }
}

//==============================================================================
void DraggableMidiFile::setMidiFile (const juce::String& path,
                                      const juce::String& displayName,
                                      const juce::String& durationText)
{
    midiFilePath = path;
    fileName = displayName;
    duration = durationText;
    isDragging = false;
    repaint();
}

void DraggableMidiFile::clear()
{
    midiFilePath = {};
    fileName = {};
    duration = {};
    isDragging = false;
    repaint();
}
