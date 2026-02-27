/*
  ==============================================================================
    PluginProcessor.h
    text2midi VST3 Plugin — Audio Processor (silence pass-through, state storage)
  ==============================================================================
*/

#pragma once

#include <juce_audio_processors/juce_audio_processors.h>

class Text2MidiProcessor : public juce::AudioProcessor
{
public:
    Text2MidiProcessor();
    ~Text2MidiProcessor() override;

    // ── AudioProcessor overrides ─────────────────────────────────────────────
    void prepareToPlay (double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;
    bool isBusesLayoutSupported (const BusesLayout& layouts) const override;
    void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    // ── Editor ───────────────────────────────────────────────────────────────
    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override { return true; }

    // ── Plugin info ──────────────────────────────────────────────────────────
    const juce::String getName() const override       { return JucePlugin_Name; }
    bool acceptsMidi() const override                 { return true; }
    bool producesMidi() const override                { return false; }
    bool isMidiEffect() const override                { return false; }
    double getTailLengthSeconds() const override      { return 0.0; }

    // ── Presets (none) ───────────────────────────────────────────────────────
    int getNumPrograms() override                     { return 1; }
    int getCurrentProgram() override                  { return 0; }
    void setCurrentProgram (int) override             {}
    const juce::String getProgramName (int) override  { return {}; }
    void changeProgramName (int, const juce::String&) override {}

    // ── State persistence ────────────────────────────────────────────────────
    void getStateInformation (juce::MemoryBlock& destData) override;
    void setStateInformation (const void* data, int sizeInBytes) override;

    // ── Plugin state accessors ───────────────────────────────────────────────
    juce::String getApiKey() const;
    void setApiKey (const juce::String& key);

    juce::String getProvider() const;
    void setProvider (const juce::String& provider);

    juce::String getCustomEndpoint() const;
    void setCustomEndpoint (const juce::String& endpoint);

    juce::String getCustomModel() const;
    void setCustomModel (const juce::String& model);

    juce::String getLastMidiPath() const;
    void setLastMidiPath (const juce::String& path);

    bool hasApiKeyConfigured() const;

private:
    // ValueTree-based state for DAW persistence
    juce::ValueTree pluginState { "Text2MidiState" };

    // Simple XOR obfuscation helpers for API key
    static juce::String obfuscate (const juce::String& plain);
    static juce::String deobfuscate (const juce::String& encoded);

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (Text2MidiProcessor)
};
