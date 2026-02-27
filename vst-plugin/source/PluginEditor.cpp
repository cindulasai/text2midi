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
    setResizable (false, false);

    auto textCol    = juce::Colour (text2midi::kColText);
    auto subtextCol = juce::Colour (text2midi::kColSubtext);

    // ── Title ────────────────────────────────────────────────────────────────
    titleLabel.setText ("text2midi", juce::dontSendNotification);
    titleLabel.setFont (juce::Font (juce::FontOptions (20.0f).withStyle ("Bold")));
    titleLabel.setColour (juce::Label::textColourId, textCol);
    titleLabel.setJustificationType (juce::Justification::centred);
    addAndMakeVisible (titleLabel);

    // ── Connection indicator ─────────────────────────────────────────────────
    connectionLabel.setText ("Checking server...", juce::dontSendNotification);
    connectionLabel.setFont (juce::Font (juce::FontOptions (11.0f)));
    connectionLabel.setColour (juce::Label::textColourId, subtextCol);
    connectionLabel.setJustificationType (juce::Justification::centred);
    addAndMakeVisible (connectionLabel);

    // ── Panels ───────────────────────────────────────────────────────────────
    apiKeyPanel.setListener (this);
    addAndMakeVisible (apiKeyPanel);

    // Show API key panel only if not yet configured
    if (processorRef.hasApiKeyConfigured())
        apiKeyPanel.setVisible (false);

    promptPanel.setListener (this);
    addAndMakeVisible (promptPanel);

    addAndMakeVisible (progressPanel);
    progressPanel.setVisible (false);

    outputPanel.setListener (this);
    addAndMakeVisible (outputPanel);
    outputPanel.setVisible (false);

    // ── Backend launch + health polling ──────────────────────────────────────
    launchBackend();
    startTimerHz (1);   // 1 Hz initially, drops to 0.2 Hz once connected
}

Text2MidiEditor::~Text2MidiEditor()
{
    stopTimer();
}

//==============================================================================
void Text2MidiEditor::paint (juce::Graphics& g)
{
    g.fillAll (juce::Colour (text2midi::kColBase));
}

void Text2MidiEditor::resized()
{
    auto area = getLocalBounds().reduced (10);

    titleLabel.setBounds (area.removeFromTop (36));
    connectionLabel.setBounds (area.removeFromTop (18));
    area.removeFromTop (6);

    if (apiKeyPanel.isVisible())
    {
        apiKeyPanel.setBounds (area.removeFromTop (200));
        area.removeFromTop (6);
    }

    promptPanel.setBounds (area.removeFromTop (100));
    area.removeFromTop (6);

    if (progressPanel.isVisible())
    {
        progressPanel.setBounds (area.removeFromTop (60));
        area.removeFromTop (6);
    }

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
        connectionLabel.setText (juce::CharPointer_UTF8 ("\xf0\x9f\x9f\xa2 Server connected"),
                                 juce::dontSendNotification);
        connectionLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColGreen));
        startTimerHz (1);   // Slow the polling once connected
    }
    else
    {
        connectionLabel.setText (juce::CharPointer_UTF8 ("\xf0\x9f\x94\xb4 Server offline"),
                                 juce::dontSendNotification);
        connectionLabel.setColour (juce::Label::textColourId, juce::Colour (text2midi::kColRed));
        startTimerHz (2);   // Poll faster when disconnected
    }
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

    // Re-check health with the new config
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

    // Simulate node-by-node progress then call generate
    juce::Thread::launch ([this, prompt]()
    {
        auto sessionId = juce::Uuid().toString().substring (0, 8);

        // Update progress on message thread
        static const juce::StringArray nodeNames {
            "Intent Parser", "Track Planner", "Theory Validator",
            "Track Generator", "Quality Control", "Refinement",
            "MIDI Creator", "Session Summary"
        };

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
