/*
  ==============================================================================
    BackendLauncher.h
    text2midi VST3 Plugin — Auto-launch Python backend server
  ==============================================================================
*/

#pragma once

#include <juce_core/juce_core.h>

class BackendLauncher
{
public:
    enum class Status
    {
        ServerAlreadyRunning,
        ServerLaunched,
        ServerNotFound,
        ServerFailedToStart
    };

    /** Attempt to launch the backend server if it's not already running.
        This is a blocking call (polls for up to 10 seconds).
        Should be called from a background thread. */
    static Status launchIfNeeded();

    /** Get a human-readable description of the status. */
    static juce::String statusToString (Status s);

private:
    /** Search for the server executable in known locations. */
    static juce::File findServerExecutable();

    BackendLauncher() = delete;
};
