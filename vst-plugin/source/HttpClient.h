/*
  ==============================================================================
    HttpClient.h
    text2midi VST3 Plugin — HTTP client for backend communication
  ==============================================================================
*/

#pragma once

#include <juce_core/juce_core.h>

class HttpClient
{
public:
    /** Check if the backend server is reachable. Thread-safe. */
    static bool checkHealth();

    /** Send a generation request. Returns JSON response as juce::var.
        Must be called from a background thread. */
    static juce::var generate (const juce::String& prompt,
                               const juce::String& sessionId);

    /** Configure the backend with API key and provider settings.
        Must be called from a background thread. */
    static bool configure (const juce::String& provider,
                           const juce::String& apiKey,
                           const juce::String& endpoint = {},
                           const juce::String& model = {});

    /** Get the full health response as JSON. Thread-safe. */
    static juce::var getHealthInfo();

private:
    /** Perform a GET request and return the response body. */
    static juce::String doGet (const juce::String& path, int timeoutMs);

    /** Perform a POST request with JSON body, return response body. */
    static juce::String doPost (const juce::String& path,
                                const juce::String& jsonBody,
                                int timeoutMs);

    HttpClient() = delete;
};
