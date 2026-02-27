/*
  ==============================================================================
    BackendLauncher.cpp
    text2midi VST3 Plugin — Backend auto-launch implementation
  ==============================================================================
*/

#include "BackendLauncher.h"
#include "HttpClient.h"
#include "PluginConfig.h"

//==============================================================================
BackendLauncher::Status BackendLauncher::launchIfNeeded()
{
    // 1. Check if server is already running
    if (HttpClient::checkHealth())
        return Status::ServerAlreadyRunning;

    // 2. Find the server executable
    auto exe = findServerExecutable();

    if (! exe.existsAsFile())
        return Status::ServerNotFound;

    // 3. Launch the process
    juce::ChildProcess process;
    bool started = process.start (exe.getFullPathName());

    if (! started)
        return Status::ServerFailedToStart;

    // 4. Poll /health until server responds (up to 10 seconds)
    int elapsed = 0;

    while (elapsed < text2midi::kBackendLaunchTimeoutMs)
    {
        juce::Thread::sleep (text2midi::kBackendPollIntervalMs);
        elapsed += text2midi::kBackendPollIntervalMs;

        if (HttpClient::checkHealth())
            return Status::ServerLaunched;
    }

    return Status::ServerFailedToStart;
}

//==============================================================================
juce::File BackendLauncher::findServerExecutable()
{
    const juce::String exeName (text2midi::kServerExeName);

    // Search location 1: Same directory as the VST3 bundle
    auto pluginDir = juce::File::getSpecialLocation (
        juce::File::currentApplicationFile).getParentDirectory();
    auto candidate1 = pluginDir.getChildFile (exeName);
    if (candidate1.existsAsFile())
        return candidate1;

    // Search location 2: Program Files
    auto candidate2 = juce::File ("C:\\Program Files\\text2midi").getChildFile (exeName);
    if (candidate2.existsAsFile())
        return candidate2;

    // Search location 3: Check PATH environment variable
    auto pathEnv = juce::SystemStats::getEnvironmentVariable ("PATH", "");
    juce::StringArray paths;
    paths.addTokens (pathEnv, ";", "");

    for (const auto& dir : paths)
    {
        auto candidate = juce::File (dir).getChildFile (exeName);
        if (candidate.existsAsFile())
            return candidate;
    }

    return {};
}

//==============================================================================
juce::String BackendLauncher::statusToString (Status s)
{
    switch (s)
    {
        case Status::ServerAlreadyRunning:  return "Server already running";
        case Status::ServerLaunched:        return "Server launched successfully";
        case Status::ServerNotFound:        return "Server executable not found";
        case Status::ServerFailedToStart:   return "Server failed to start";
    }

    return "Unknown";
}
