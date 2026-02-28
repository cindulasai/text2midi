/*
  ==============================================================================
    PromptPanel.h
    text2midi VST3 Plugin — Prompt input + generate button
  ==============================================================================
*/

#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

class PromptPanel : public juce::Component,
                    public juce::Button::Listener,
                    public juce::TextEditor::Listener
{
public:
    PromptPanel();
    ~PromptPanel() override;

    void resized() override;
    void paint (juce::Graphics& g) override;
    void buttonClicked (juce::Button* button) override;

    /** Called when the user types in the prompt editor. */
    void textEditorTextChanged (juce::TextEditor&) override;

    /** Set whether generation is in progress (disables controls). */
    void setGenerating (bool generating);

    /** Set whether the backend is connected (enables/disables generate). */
    void setConnected (bool connected);

    /** Set the prompt text (used by genre presets). */
    void setPromptText (const juce::String& text);

    /** Get the current prompt text. */
    juce::String getPromptText() const;

    /** Display the active model info. */
    void setModelInfo (const juce::String& provider, const juce::String& model);

    /** Listener for generate requests. */
    class Listener
    {
    public:
        virtual ~Listener() = default;
        virtual void generateRequested (const juce::String& prompt) = 0;
    };

    void setListener (Listener* l) { listener = l; }

private:
    Listener* listener = nullptr;

    juce::Label       modelInfoLabel;
    juce::TextEditor  promptEditor;
    juce::TextButton  generateButton { "Generate" };

    bool isGenerating = false;
    bool isConnected  = false;

    void updateButtonState();

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (PromptPanel)
};
