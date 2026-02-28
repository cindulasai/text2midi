/*
  ==============================================================================
    PluginEditor.cpp
    text2midi VST3 Plugin — Main plugin UI implementation
  ==============================================================================
*/

#include "PluginEditor.h"
#include "BackendLauncher.h"
#include "HttpClient.h"
#include "PluginConfig.h"

//==============================================================================
Text2MidiEditor::Text2MidiEditor (Text2MidiProcessor& p)
    : AudioProcessorEditor (&p),
      processorRef (p),
      apiKeyPanel (p)
{
    setSize (text2midi::kPluginWidth, text2midi::kPluginHeight);
    setResizable (true, true);
    setResizeLimits (500, 600, 900, 1200);

    auto textCol    = juce::Colour (text2midi::kColText);
    auto subtextCol = juce::Colour (text2midi::kColSubtext);

    // ── Title ────────────────────────────────────────────────────────────────
    titleLabel.setText ("text2midi", juce::dontSendNotification);
    titleLabel.setFont (juce::Font (juce::FontOptions (22.0f).withStyle ("Bold")));
    titleLabel.setColour (juce::Label::textColourId, textCol);
    titleLabel.setJustificationType (juce::Justification::centredLeft);
    addAndMakeVisible (titleLabel);

    // ── Subtitle ─────────────────────────────────────────────────────────────
    subtitleLabel.setText ("AI-Powered MIDI Composer", juce::dontSendNotification);
    subtitleLabel.setFont (juce::Font (juce::FontOptions (11.0f)));
    subtitleLabel.setColour (juce::Label::textColourId, subtextCol);
    subtitleLabel.setJustificationType (juce::Justification::centredLeft);
    addAndMakeVisible (subtitleLabel);

    // ── Version ──────────────────────────────────────────────────────────────
    versionLabel.setText (juce::String ("v") + text2midi::kPluginVersion, juce::dontSendNotification);
    versionLabel.setFont (juce::Font (juce::FontOptions (10.0f)));
    versionLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColOverlay0));
    versionLabel.setJustificationType (juce::Justification::centredRight);
    addAndMakeVisible (versionLabel);

    // ── Connection indicator ─────────────────────────────────────────────────
    connectionLabel.setText ("Connecting to server...", juce::dontSendNotification);
    connectionLabel.setFont (juce::Font (juce::FontOptions (11.0f)));
    connectionLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColYellow));
    connectionLabel.setJustificationType (juce::Justification::centredRight);
    addAndMakeVisible (connectionLabel);

    // ── Panels ───────────────────────────────────────────────────────────────
    apiKeyPanel.setListener (this);
    addAndMakeVisible (apiKeyPanel);

    // Show API key panel only if not yet configured
    if (processorRef.hasApiKeyConfigured())
        apiKeyPanel.setVisible (false);

    genrePresetPanel.setListener (this);
    addAndMakeVisible (genrePresetPanel);

    promptPanel.setListener (this);
    addAndMakeVisible (promptPanel);

    addAndMakeVisible (progressPanel);
    progressPanel.setVisible (false);

    outputPanel.setListener (this);
    addAndMakeVisible (outputPanel);
    outputPanel.setVisible (false);

    // ── Backend launch + health polling ──────────────────────────────────────
    launchBackend();
    startTimerHz (1);
}

Text2MidiEditor::~Text2MidiEditor()
{
    stopTimer();
}

//==============================================================================
void Text2MidiEditor::paint (juce::Graphics& g)
{
    g.fillAll (juce::Colour (text2midi::kColBase));

    // Subtle top gradient for header area
    auto headerArea = getLocalBounds().removeFromTop (56).toFloat();
    juce::ColourGradient headerGrad (
        juce::Colour (text2midi::kColSurface0).withAlpha (0.5f), 0, 0,
        juce::Colour (text2midi::kColBase), 0, headerArea.getBottom(),
        false);
    g.setGradientFill (headerGrad);
    g.fillRect (headerArea);
}

void Text2MidiEditor::resized()
{
    auto area = getLocalBounds().reduced (12);

    // Header: title + subtitle on left, version + connection on right
    auto headerRow = area.removeFromTop (28);
    titleLabel.setBounds (headerRow.removeFromLeft (200));
    versionLabel.setBounds (headerRow.removeFromRight (60));
    connectionLabel.setBounds (headerRow);

    subtitleLabel.setBounds (area.removeFromTop (16));
    area.removeFromTop (8);

    // API key panel (conditionally visible)
    if (apiKeyPanel.isVisible())
    {
        apiKeyPanel.setBounds (area.removeFromTop (200));
        area.removeFromTop (6);
    }

    // Genre presets
    genrePresetPanel.setBounds (area.removeFromTop (90));
    area.removeFromTop (6);

    // Prompt panel
    promptPanel.setBounds (area.removeFromTop (130));
    area.removeFromTop (6);

    // Progress panel (conditionally visible)
    if (progressPanel.isVisible())
    {
        progressPanel.setBounds (area.removeFromTop (60));
        area.removeFromTop (6);
    }

    // Output panel fills remaining space
    if (outputPanel.isVisible())
    {
        outputPanel.setBounds (area);
    }
}

//==============================================================================
// Timer — health check polling
//==============================================================================

void Text2MidiEditor::timerCallback()
{
    juce::Thread::launch ([this]()
    {
        bool healthy = HttpClient::checkHealth();

        juce::MessageManager::callAsync ([this, healthy]()
        {
            updateConnectionStatus (healthy);
        });
    });
}

void Text2MidiEditor::updateConnectionStatus (bool connected)
{
    if (backendConnected == connected)
        return;

    backendConnected = connected;
    promptPanel.setConnected (connected);

    if (connected)
    {
        connectionLabel.setText (juce::CharPointer_UTF8 ("\xf0\x9f\x9f\xa2 Connected"),
                                 juce::dontSendNotification);
        connectionLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColGreen));
        startTimerHz (1);

        // Fetch model info from backend
        fetchModelInfo();
    }
    else
    {
        connectionLabel.setText (juce::CharPointer_UTF8 ("\xf0\x9f\x94\xb4 Server offline"),
                                 juce::dontSendNotification);
        connectionLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColRed));
        startTimerHz (2);
    }
}

//==============================================================================
// Fetch model info from backend /health endpoint
//==============================================================================

void Text2MidiEditor::fetchModelInfo()
{
    juce::Thread::launch ([this]()
    {
        auto healthInfo = HttpClient::getHealthInfo();

        if (! healthInfo.isVoid())
        {
            auto provider = healthInfo.getProperty ("provider", "").toString();
            auto version  = healthInfo.getProperty ("version", "").toString();

            juce::MessageManager::callAsync ([this, provider, version]()
            {
                if (provider.isNotEmpty())
                    promptPanel.setModelInfo (provider, version);
            });
        }
    });
}

//==============================================================================
// Backend launcher
//==============================================================================

void Text2MidiEditor::launchBackend()
{
    juce::Thread::launch ([this]()
    {
        auto status = BackendLauncher::launchIfNeeded();

        juce::MessageManager::callAsync ([this, status]()
        {
            bool connected = (status == BackendLauncher::Status::ServerAlreadyRunning
                           || status == BackendLauncher::Status::ServerLaunched);
            updateConnectionStatus (connected);
        });
    });
}

//==============================================================================
// Panel callbacks
//==============================================================================

void Text2MidiEditor::apiKeyConfigured()
{
    apiKeyPanel.setVisible (false);
    resized();

    // Re-check health with the new config and fetch model info
    juce::Thread::launch ([this]()
    {
        bool healthy = HttpClient::checkHealth();
        juce::MessageManager::callAsync ([this, healthy]()
        {
            updateConnectionStatus (healthy);
        });
    });
}

void Text2MidiEditor::generateRequested (const juce::String& prompt)
{
    promptPanel.setGenerating (true);
    progressPanel.show();
    outputPanel.clear();
    resized();

    juce::Thread::launch ([this, prompt]()
    {
        auto sessionId = juce::Uuid().toString().substring (0, 8);

        auto result = HttpClient::generate (prompt, sessionId);

        juce::MessageManager::callAsync ([this, result]()
        {
            promptPanel.setGenerating (false);

            if (result.isVoid() || result.getProperty ("status", "").toString() == "error")
            {
                auto error = result.isVoid() ? "Server unreachable"
                    : result.getProperty ("detail",
                        result.getProperty ("error", "Unknown error")).toString();
                progressPanel.markError (error);
            }
            else
            {
                auto quality = static_cast<float> (result.getProperty ("quality_score", 0.0));
                progressPanel.markComplete (quality);

                outputPanel.setResult (result);

                // Store last MIDI path
                auto midiPath = result.getProperty ("midi_path", "").toString();
                if (midiPath.isNotEmpty())
                    processorRef.setLastMidiPath (midiPath);
            }

            resized();
        });
    });
}

void Text2MidiEditor::changeApiKeyRequested()
{
    apiKeyPanel.setVisible (true);
    apiKeyPanel.loadFromState();
    resized();
}

void Text2MidiEditor::genrePresetSelected (const juce::String& prompt)
{
    promptPanel.setPromptText (prompt);
}
