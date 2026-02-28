/*
  ==============================================================================
    PluginEditor.h
    text2midi VST3 Plugin — Main plugin UI
  ==============================================================================
*/

#pragma once

#include "ApiKeyPanel.h"
#include "GenrePresetPanel.h"
#include "OutputPanel.h"
#include "PluginProcessor.h"
#include "ProgressPanel.h"
#include "PromptPanel.h"
#include <juce_gui_extra/juce_gui_extra.h>

class Text2MidiEditor : public juce::AudioProcessorEditor,
                         public juce::DragAndDropContainer,
                         public juce::Timer,
                         public ApiKeyPanel::Listener,
                         public PromptPanel::Listener,
                         public OutputPanel::Listener,
                         public GenrePresetPanel::Listener
{
public:
    explicit Text2MidiEditor (Text2MidiProcessor&);
    ~Text2MidiEditor() override;

    void paint (juce::Graphics&) override;
    void resized() override;

    // ── Timer (health check polling) ─────────────────────────────────────────
    void timerCallback() override;

    // ── Panel callbacks ──────────────────────────────────────────────────────
    void apiKeyConfigured() override;
    void generateRequested (const juce::String& prompt) override;
    void changeApiKeyRequested() override;
    void genrePresetSelected (const juce::String& prompt) override;

private:
    Text2MidiProcessor& processorRef;

    // ── UI components ────────────────────────────────────────────────────────
    juce::Label         titleLabel;
    juce::Label         subtitleLabel;
    juce::Label         connectionLabel;
    juce::Label         versionLabel;
    ApiKeyPanel         apiKeyPanel;
    GenrePresetPanel    genrePresetPanel;
    PromptPanel         promptPanel;
    ProgressPanel       progressPanel;
    OutputPanel         outputPanel;

    // ── State ────────────────────────────────────────────────────────────────
    bool backendConnected = false;

    void updateConnectionStatus (bool connected);
    void launchBackend();
    void fetchModelInfo();

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (Text2MidiEditor)
};
