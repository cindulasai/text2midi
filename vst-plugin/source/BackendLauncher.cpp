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

    // 2. Try compiled executable first
    auto exe = findServerExecutable();
    bool started = false;

    juce::ChildProcess process;

    if (exe.existsAsFile())
    {
        started = process.start (exe.getFullPathName());
    }

    // 3. If no exe (or exe failed), try Python fallback
    if (! started)
    {
        started = launchPythonServer (process);
    }

    if (! started)
        return Status::ServerNotFound;

    // 4. Poll /health until server responds (up to 15 seconds for Python startup)
    int elapsed = 0;
    constexpr int pythonTimeoutMs = 15000; // Python startup can be slower

    while (elapsed < pythonTimeoutMs)
    {
        juce::Thread::sleep (text2midi::kBackendPollIntervalMs);
        elapsed += text2midi::kBackendPollIntervalMs;

        if (HttpClient::checkHealth())
            return Status::ServerLaunched;
    }

    return Status::ServerFailedToStart;
}

//==============================================================================
bool BackendLauncher::launchPythonServer (juce::ChildProcess& process)
{
    auto projectRoot = findProjectRoot();

    if (! projectRoot.isDirectory())
        return false;

    // The server script lives at: <projectRoot>/vst-plugin/python-backend/server.py
    auto serverScript = projectRoot.getChildFile ("vst-plugin")
                                   .getChildFile ("python-backend")
                                   .getChildFile ("server.py");

    if (! serverScript.existsAsFile())
        return false;

    // Strategy 1: Try "uv run python server.py" (best for managed environments)
    auto uv = findOnPath ("uv");
    if (uv.existsAsFile())
    {
        juce::String cmd = "\"" + uv.getFullPathName() + "\" run python \""
                         + serverScript.getFullPathName() + "\"";
        if (process.start (cmd))
            return true;
    }

    // Strategy 2: Try "python server.py" directly
   #if JUCE_WINDOWS
    juce::StringArray pythonNames { "python", "python3", "py" };
   #else
    juce::StringArray pythonNames { "python3", "python" };
   #endif

    for (const auto& pyName : pythonNames)
    {
        auto py = findOnPath (pyName);
        if (py.existsAsFile())
        {
            juce::String cmd = "\"" + py.getFullPathName() + "\" \""
                             + serverScript.getFullPathName() + "\"";
            if (process.start (cmd))
                return true;
        }
    }

    return false;
}

//==============================================================================
juce::File BackendLauncher::findProjectRoot()
{
    // Strategy 1: Walk up from the VST3 plugin bundle location
    auto pluginDir = juce::File::getSpecialLocation (
        juce::File::currentApplicationFile).getParentDirectory();

    // Walk up the directory tree looking for a marker file (pyproject.toml or main.py)
    auto dir = pluginDir;
    for (int i = 0; i < 8; ++i)
    {
        if (dir.getChildFile ("pyproject.toml").existsAsFile()
            || dir.getChildFile ("main.py").existsAsFile())
            return dir;
        dir = dir.getParentDirectory();
    }

    // Strategy 2: Check well-known development paths
   #if JUCE_WINDOWS
    // Common Windows dev locations
    auto userDocs = juce::File::getSpecialLocation (juce::File::userDocumentsDirectory);
    auto githubDir = userDocs.getChildFile ("GitHub").getChildFile ("spec-kit");
    if (githubDir.getChildFile ("pyproject.toml").existsAsFile())
        return githubDir;

    auto oneDriveDocs = juce::File::getSpecialLocation (juce::File::userHomeDirectory)
                            .getChildFile ("OneDrive").getChildFile ("Documents")
                            .getChildFile ("GitHub").getChildFile ("spec-kit");
    if (oneDriveDocs.getChildFile ("pyproject.toml").existsAsFile())
        return oneDriveDocs;
   #else
    // macOS / Linux
    auto homeGithub = juce::File::getSpecialLocation (juce::File::userHomeDirectory)
                          .getChildFile ("GitHub").getChildFile ("spec-kit");
    if (homeGithub.getChildFile ("pyproject.toml").existsAsFile())
        return homeGithub;
   #endif

    return {};
}

//==============================================================================
juce::File BackendLauncher::findOnPath (const juce::String& name)
{
   #if JUCE_WINDOWS
    juce::String exeName = name.endsWith (".exe") ? name : name + ".exe";
   #else
    juce::String exeName = name;
   #endif

    auto pathEnv = juce::SystemStats::getEnvironmentVariable ("PATH", "");
    juce::StringArray paths;
   #if JUCE_WINDOWS
    paths.addTokens (pathEnv, ";", "");
   #else
    paths.addTokens (pathEnv, ":", "");
   #endif

    for (const auto& dir : paths)
    {
        auto candidate = juce::File (dir).getChildFile (exeName);
        if (candidate.existsAsFile())
            return candidate;
    }

    return {};
}

//==============================================================================
juce::File BackendLauncher::findServerExecutable()
{
   #if JUCE_WINDOWS
    const juce::String exeName ("text2midi-backend.exe");
   #else
    const juce::String exeName ("text2midi-backend");
   #endif

    // Search location 1: Same directory as the VST3 bundle
    auto pluginDir = juce::File::getSpecialLocation (
        juce::File::currentApplicationFile).getParentDirectory();
    auto candidate1 = pluginDir.getChildFile (exeName);
    if (candidate1.existsAsFile())
        return candidate1;

   #if JUCE_WINDOWS
    // Search location 2: Program Files (Windows)
    auto candidate2 = juce::File ("C:\\Program Files\\text2midi").getChildFile (exeName);
    if (candidate2.existsAsFile())
        return candidate2;
   #elif JUCE_MAC
    // Search location 2: /usr/local/lib (macOS)
    auto candidate2 = juce::File ("/usr/local/lib/text2midi-backend").getChildFile (exeName);
    if (candidate2.existsAsFile())
        return candidate2;
   #else
    // Search location 2: ~/.local/lib (Linux)
    auto candidate2 = juce::File::getSpecialLocation (juce::File::userHomeDirectory)
        .getChildFile (".local/lib/text2midi-backend").getChildFile (exeName);
    if (candidate2.existsAsFile())
        return candidate2;
   #endif

    // Search location 3: Check PATH
    return findOnPath (exeName.trimCharactersAtEnd (".exe"));
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
