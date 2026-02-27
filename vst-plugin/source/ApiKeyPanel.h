/*
  ==============================================================================
    ApiKeyPanel.h
    text2midi VST3 Plugin — API key configuration panel
  ==============================================================================
*/

#pragma once

#include <juce_gui_basics/juce_gui_basics.h>

class Text2MidiProcessor;

class ApiKeyPanel : public juce::Component,
                    public juce::Button::Listener,
                    public juce::ComboBox::Listener
{
public:
    explicit ApiKeyPanel (Text2MidiProcessor& processor);

    void resized() override;
    void paint (juce::Graphics& g) override;

    // ── Callbacks ────────────────────────────────────────────────────────────
    void buttonClicked (juce::Button* button) override;
    void comboBoxChanged (juce::ComboBox* comboBox) override;

    /** Listener for when configuration completes. */
    class Listener
    {
    public:
        virtual ~Listener() = default;
        virtual void apiKeyConfigured() = 0;
    };

    void setListener (Listener* l) { listener = l; }

    /** Populate fields from processor state. */
    void loadFromState();

private:
    Text2MidiProcessor& processor;
    Listener* listener = nullptr;

    juce::Label         titleLabel;
    juce::Label         providerLabel;
    juce::ComboBox      providerCombo;
    juce::Label         apiKeyLabel;
    juce::TextEditor    apiKeyEditor;
    juce::Label         endpointLabel;
    juce::TextEditor    endpointEditor;
    juce::Label         modelLabel;
    juce::TextEditor    modelEditor;
    juce::TextButton    saveButton { "Save & Connect" };

    void updateCustomFieldsVisibility();

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (ApiKeyPanel)
};
