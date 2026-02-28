/*
  ==============================================================================
    PromptPanel.cpp
    text2midi VST3 Plugin — Prompt input + generate button implementation
  ==============================================================================
*/

#include "PromptPanel.h"
#include "PluginConfig.h"

//==============================================================================
PromptPanel::PromptPanel()
{
    auto textCol    = juce::Colour (text2midi::kColText);
    auto subtextCol = juce::Colour (text2midi::kColSubtext);

    // Model info display
    modelInfoLabel.setText ("", juce::dontSendNotification);
    modelInfoLabel.setFont (juce::Font (juce::FontOptions (11.0f)));
    modelInfoLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColOverlay0));
    modelInfoLabel.setJustificationType (juce::Justification::centredRight);
    addAndMakeVisible (modelInfoLabel);

    // Multi-line prompt input
    promptEditor.setMultiLine (true, true);
    promptEditor.setReturnKeyStartsNewLine (false);
    promptEditor.setTextToShowWhenEmpty (
        "Describe your music... e.g. 'dreamy jazz with piano and soft drums'\n"
        "Be specific: mention instruments, mood, tempo, genre, key...",
        subtextCol);
    promptEditor.setColour (juce::TextEditor::backgroundColourId, juce::Colour (text2midi::kColSurface1));
    promptEditor.setColour (juce::TextEditor::textColourId, textCol);
    promptEditor.setColour (juce::TextEditor::outlineColourId, juce::Colours::transparentBlack);
    promptEditor.setFont (juce::Font (juce::FontOptions (14.0f)));
    promptEditor.addListener (this);
    addAndMakeVisible (promptEditor);

    // Generate button
    generateButton.setColour (juce::TextButton::buttonColourId, juce::Colour (text2midi::kColBlue));
    generateButton.setColour (juce::TextButton::textColourOnId, juce::Colour (text2midi::kColBase));
    generateButton.setColour (juce::TextButton::textColourOffId, juce::Colour (text2midi::kColBase));
    generateButton.addListener (this);
    addAndMakeVisible (generateButton);

    updateButtonState();
}

PromptPanel::~PromptPanel()
{
    promptEditor.removeListener (this);
}

//==============================================================================
void PromptPanel::textEditorTextChanged (juce::TextEditor&)
{
    updateButtonState();
}

//==============================================================================
void PromptPanel::paint (juce::Graphics& g)
{
    g.setColour (juce::Colour (text2midi::kColSurface0));
    g.fillRoundedRectangle (getLocalBounds().toFloat(), 6.0f);
}

void PromptPanel::resized()
{
    auto area = getLocalBounds().reduced (10);

    modelInfoLabel.setBounds (area.removeFromTop (16));
    area.removeFromTop (2);
    generateButton.setBounds (area.removeFromBottom (36));
    area.removeFromBottom (6);
    promptEditor.setBounds (area);
}

//==============================================================================
void PromptPanel::buttonClicked (juce::Button* button)
{
    if (button == &generateButton && listener != nullptr)
    {
        auto prompt = promptEditor.getText().trim();
        if (prompt.isNotEmpty())
            listener->generateRequested (prompt);
    }
}

//==============================================================================
void PromptPanel::setGenerating (bool generating)
{
    isGenerating = generating;
    generateButton.setButtonText (generating ? "Generating..." : "Generate");
    updateButtonState();
}

void PromptPanel::setConnected (bool connected)
{
    isConnected = connected;
    updateButtonState();
}

void PromptPanel::setPromptText (const juce::String& text)
{
    promptEditor.setText (text, juce::dontSendNotification);
    updateButtonState();
}

juce::String PromptPanel::getPromptText() const
{
    return promptEditor.getText().trim();
}

void PromptPanel::setModelInfo (const juce::String& provider, const juce::String& model)
{
    auto info = provider.toUpperCase() + " / " + model;
    modelInfoLabel.setText (info, juce::dontSendNotification);
}

void PromptPanel::updateButtonState()
{
    bool canGenerate = isConnected
                    && ! isGenerating
                    && promptEditor.getText().trim().isNotEmpty();

    generateButton.setEnabled (canGenerate);
    generateButton.setAlpha (canGenerate ? 1.0f : 0.5f);
}
