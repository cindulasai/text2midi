/*
  ==============================================================================
    ApiKeyPanel.cpp
    text2midi VST3 Plugin — API key configuration panel implementation
  ==============================================================================
*/

#include "ApiKeyPanel.h"
#include "HttpClient.h"
#include "PluginConfig.h"
#include "PluginProcessor.h"

//==============================================================================
ApiKeyPanel::ApiKeyPanel (Text2MidiProcessor& p)
    : processor (p)
{
    auto textCol = juce::Colour (text2midi::kColText);
    auto subtextCol = juce::Colour (text2midi::kColSubtext);

    // Title
    titleLabel.setText ("API Key Setup", juce::dontSendNotification);
    titleLabel.setFont (juce::Font (juce::FontOptions (16.0f).withStyle ("Bold")));
    titleLabel.setColour (juce::Label::textColourId, textCol);
    addAndMakeVisible (titleLabel);

    // Provider selector
    providerLabel.setText ("Provider:", juce::dontSendNotification);
    providerLabel.setColour (juce::Label::textColourId, subtextCol);
    addAndMakeVisible (providerLabel);

    providerCombo.addItem ("MiniMax M2.5",      1);
    providerCombo.addItem ("Groq (Llama)",       2);
    providerCombo.addItem ("OpenAI-compatible",  3);
    providerCombo.addItem ("Custom Endpoint",    4);
    providerCombo.setSelectedId (1, juce::dontSendNotification);
    providerCombo.addListener (this);
    addAndMakeVisible (providerCombo);

    // API Key
    apiKeyLabel.setText ("API Key:", juce::dontSendNotification);
    apiKeyLabel.setColour (juce::Label::textColourId, subtextCol);
    addAndMakeVisible (apiKeyLabel);

    apiKeyEditor.setPasswordCharacter (L'\u2022'); // bullet •
    apiKeyEditor.setTextToShowWhenEmpty ("Enter your API key...", subtextCol);
    addAndMakeVisible (apiKeyEditor);

    // Custom endpoint (conditionally visible)
    endpointLabel.setText ("Endpoint:", juce::dontSendNotification);
    endpointLabel.setColour (juce::Label::textColourId, subtextCol);
    addAndMakeVisible (endpointLabel);

    endpointEditor.setTextToShowWhenEmpty ("https://api.example.com/v1", subtextCol);
    addAndMakeVisible (endpointEditor);

    // Custom model
    modelLabel.setText ("Model:", juce::dontSendNotification);
    modelLabel.setColour (juce::Label::textColourId, subtextCol);
    addAndMakeVisible (modelLabel);

    modelEditor.setTextToShowWhenEmpty ("gpt-4o", subtextCol);
    addAndMakeVisible (modelEditor);

    // Save button
    saveButton.setColour (juce::TextButton::buttonColourId,
                          juce::Colour (text2midi::kColBlue));
    saveButton.setColour (juce::TextButton::textColourOnId,
                          juce::Colour (text2midi::kColBase));
    saveButton.addListener (this);
    addAndMakeVisible (saveButton);

    updateCustomFieldsVisibility();
    loadFromState();
}

//==============================================================================
void ApiKeyPanel::paint (juce::Graphics& g)
{
    g.setColour (juce::Colour (text2midi::kColSurface0));
    g.fillRoundedRectangle (getLocalBounds().toFloat(), 6.0f);
}

void ApiKeyPanel::resized()
{
    auto area = getLocalBounds().reduced (12);
    auto rowH = 28;
    auto gap = 4;

    titleLabel.setBounds (area.removeFromTop (rowH));
    area.removeFromTop (gap);

    auto providerRow = area.removeFromTop (rowH);
    providerLabel.setBounds (providerRow.removeFromLeft (70));
    providerCombo.setBounds (providerRow);
    area.removeFromTop (gap);

    auto keyRow = area.removeFromTop (rowH);
    apiKeyLabel.setBounds (keyRow.removeFromLeft (70));
    apiKeyEditor.setBounds (keyRow);
    area.removeFromTop (gap);

    auto endpointRow = area.removeFromTop (rowH);
    endpointLabel.setBounds (endpointRow.removeFromLeft (70));
    endpointEditor.setBounds (endpointRow);
    area.removeFromTop (gap);

    auto modelRow = area.removeFromTop (rowH);
    modelLabel.setBounds (modelRow.removeFromLeft (70));
    modelEditor.setBounds (modelRow);
    area.removeFromTop (gap * 2);

    saveButton.setBounds (area.removeFromTop (32));
}

//==============================================================================
void ApiKeyPanel::comboBoxChanged (juce::ComboBox*)
{
    updateCustomFieldsVisibility();
}

void ApiKeyPanel::buttonClicked (juce::Button* button)
{
    if (button != &saveButton)
        return;

    // Map combo selection to provider IDs used by backend
    static const juce::StringArray providerIds { "", "minimax", "groq", "openai_custom", "openai_custom" };
    int idx = providerCombo.getSelectedId();
    auto provider = (idx >= 1 && idx <= 4) ? providerIds[idx] : juce::String ("minimax");

    auto apiKey   = apiKeyEditor.getText().trim();
    auto endpoint = endpointEditor.getText().trim();
    auto model    = modelEditor.getText().trim();

    if (apiKey.isEmpty())
        return;

    // Store in processor state (persisted with DAW project)
    processor.setProvider (provider);
    processor.setApiKey (apiKey);
    processor.setCustomEndpoint (endpoint);
    processor.setCustomModel (model);

    // Configure the backend on a background thread
    juce::Thread::launch ([this, provider, apiKey, endpoint, model]()
    {
        bool success = HttpClient::configure (provider, apiKey, endpoint, model);

        juce::MessageManager::callAsync ([this, success]()
        {
            if (success && listener != nullptr)
                listener->apiKeyConfigured();
        });
    });
}

//==============================================================================
void ApiKeyPanel::loadFromState()
{
    auto provider = processor.getProvider();
    auto apiKey   = processor.getApiKey();
    auto endpoint = processor.getCustomEndpoint();
    auto model    = processor.getCustomModel();

    // Set combo to matching provider
    if (provider == "minimax")          providerCombo.setSelectedId (1, juce::dontSendNotification);
    else if (provider == "groq")        providerCombo.setSelectedId (2, juce::dontSendNotification);
    else if (provider == "openai_custom") providerCombo.setSelectedId (3, juce::dontSendNotification);
    else                                 providerCombo.setSelectedId (1, juce::dontSendNotification);

    if (apiKey.isNotEmpty())
        apiKeyEditor.setText (apiKey, juce::dontSendNotification);

    if (endpoint.isNotEmpty())
        endpointEditor.setText (endpoint, juce::dontSendNotification);

    if (model.isNotEmpty())
        modelEditor.setText (model, juce::dontSendNotification);

    updateCustomFieldsVisibility();
}

void ApiKeyPanel::updateCustomFieldsVisibility()
{
    bool showCustom = (providerCombo.getSelectedId() >= 3);
    endpointLabel.setVisible (showCustom);
    endpointEditor.setVisible (showCustom);
    modelLabel.setVisible (showCustom);
    modelEditor.setVisible (showCustom);
}
