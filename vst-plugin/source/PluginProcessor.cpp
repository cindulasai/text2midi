/*
  ==============================================================================
    PluginProcessor.cpp
    text2midi VST3 Plugin — Audio Processor Implementation
  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"
#include "PluginConfig.h"

//==============================================================================
Text2MidiProcessor::Text2MidiProcessor()
    : AudioProcessor (BusesProperties()
                        .withOutput ("Output", juce::AudioChannelSet::stereo(), true))
{
}

Text2MidiProcessor::~Text2MidiProcessor() {}

//==============================================================================
void Text2MidiProcessor::prepareToPlay (double /*sampleRate*/, int /*samplesPerBlock*/)
{
    // No audio processing needed — this is a UI-only tool.
}

void Text2MidiProcessor::releaseResources() {}

bool Text2MidiProcessor::isBusesLayoutSupported (const BusesLayout& layouts) const
{
    // Only support stereo output
    if (layouts.getMainOutputChannelSet() != juce::AudioChannelSet::stereo())
        return false;

    return true;
}

void Text2MidiProcessor::processBlock (juce::AudioBuffer<float>& buffer,
                                        juce::MidiBuffer& /*midiMessages*/)
{
    // Clear audio — this plugin outputs silence
    buffer.clear();
}

//==============================================================================
juce::AudioProcessorEditor* Text2MidiProcessor::createEditor()
{
    return new Text2MidiEditor (*this);
}

//==============================================================================
// State persistence — stores API key, provider, endpoint, model, last MIDI path
//==============================================================================

void Text2MidiProcessor::getStateInformation (juce::MemoryBlock& destData)
{
    auto xml = pluginState.createXml();
    if (xml != nullptr)
        copyXmlToBinary (*xml, destData);
}

void Text2MidiProcessor::setStateInformation (const void* data, int sizeInBytes)
{
    auto xml = getXmlFromBinary (data, sizeInBytes);
    if (xml != nullptr && xml->hasTagName (pluginState.getType()))
        pluginState = juce::ValueTree::fromXml (*xml);
}

//==============================================================================
// State accessors
//==============================================================================

juce::String Text2MidiProcessor::getApiKey() const
{
    auto encoded = pluginState.getProperty ("api_key", "").toString();
    return encoded.isEmpty() ? juce::String() : deobfuscate (encoded);
}

void Text2MidiProcessor::setApiKey (const juce::String& key)
{
    pluginState.setProperty ("api_key", obfuscate (key), nullptr);
}

juce::String Text2MidiProcessor::getProvider() const
{
    return pluginState.getProperty ("provider", "").toString();
}

void Text2MidiProcessor::setProvider (const juce::String& provider)
{
    pluginState.setProperty ("provider", provider, nullptr);
}

juce::String Text2MidiProcessor::getCustomEndpoint() const
{
    return pluginState.getProperty ("custom_endpoint", "").toString();
}

void Text2MidiProcessor::setCustomEndpoint (const juce::String& endpoint)
{
    pluginState.setProperty ("custom_endpoint", endpoint, nullptr);
}

juce::String Text2MidiProcessor::getCustomModel() const
{
    return pluginState.getProperty ("custom_model", "").toString();
}

void Text2MidiProcessor::setCustomModel (const juce::String& model)
{
    pluginState.setProperty ("custom_model", model, nullptr);
}

juce::String Text2MidiProcessor::getLastMidiPath() const
{
    return pluginState.getProperty ("last_midi_path", "").toString();
}

void Text2MidiProcessor::setLastMidiPath (const juce::String& path)
{
    pluginState.setProperty ("last_midi_path", path, nullptr);
}

bool Text2MidiProcessor::hasApiKeyConfigured() const
{
    return getApiKey().isNotEmpty() && getProvider().isNotEmpty();
}

//==============================================================================
// Simple XOR + Base64 obfuscation for API key
// NOTE: This is NOT encryption — it prevents plain-text exposure in DAW project
// files but does NOT protect against a determined attacker.
//==============================================================================

static constexpr char kXorKey[] = "t2m_obfuscation_key_v1";

juce::String Text2MidiProcessor::obfuscate (const juce::String& plain)
{
    auto bytes = plain.toUTF8();
    juce::MemoryBlock block (bytes.getAddress(), bytes.sizeInBytes());
    auto* data = static_cast<char*> (block.getData());
    size_t keyLen = sizeof (kXorKey) - 1;

    for (size_t i = 0; i < block.getSize(); ++i)
        data[i] ^= kXorKey[i % keyLen];

    return block.toBase64Encoding();
}

juce::String Text2MidiProcessor::deobfuscate (const juce::String& encoded)
{
    juce::MemoryBlock block;
    if (! block.fromBase64Encoding (encoded))
        return {};

    auto* data = static_cast<char*> (block.getData());
    size_t keyLen = sizeof (kXorKey) - 1;

    for (size_t i = 0; i < block.getSize(); ++i)
        data[i] ^= kXorKey[i % keyLen];

    return juce::String::fromUTF8 (static_cast<const char*> (block.getData()),
                                    (int) block.getSize());
}

//==============================================================================
// This creates new instances of the plugin
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new Text2MidiProcessor();
}
