/*
  ==============================================================================
    HttpClient.cpp
    text2midi VST3 Plugin — HTTP client implementation using juce::URL
  ==============================================================================
*/

#include "HttpClient.h"
#include "PluginConfig.h"

//==============================================================================
// Helpers
//==============================================================================

static juce::String buildUrl (const juce::String& path)
{
    return juce::String (text2midi::kBackendBaseUrl) + path;
}

//==============================================================================
juce::String HttpClient::doGet (const juce::String& path, int timeoutMs)
{
    juce::URL url (buildUrl (path));

    auto options = juce::URL::InputStreamOptions (juce::URL::ParameterHandling::inAddress)
                       .withConnectionTimeoutMs (timeoutMs);

    auto stream = url.createInputStream (options);

    if (stream == nullptr)
        return {};

    return stream->readEntireStreamAsString();
}

juce::String HttpClient::doPost (const juce::String& path,
                                  const juce::String& jsonBody,
                                  int timeoutMs)
{
    juce::URL url (buildUrl (path));
    url = url.withPOSTData (jsonBody);

    juce::URL::InputStreamOptions options (juce::URL::ParameterHandling::inPostData);
    auto stream = url.createInputStream (options.withConnectionTimeoutMs (timeoutMs)
                                                .withExtraHeaders ("Content-Type: application/json"));

    if (stream == nullptr)
        return {};

    return stream->readEntireStreamAsString();
}

//==============================================================================
// Public API
//==============================================================================

bool HttpClient::checkHealth()
{
    auto response = doGet ("/health", text2midi::kHealthTimeoutMs);

    if (response.isEmpty())
        return false;

    auto json = juce::JSON::parse (response);
    return json.getProperty ("status", "").toString() == "ok";
}

juce::var HttpClient::getHealthInfo()
{
    auto response = doGet ("/health", text2midi::kHealthTimeoutMs);

    if (response.isEmpty())
        return {};

    return juce::JSON::parse (response);
}

juce::var HttpClient::generate (const juce::String& prompt,
                                 const juce::String& sessionId)
{
    juce::DynamicObject::Ptr obj = new juce::DynamicObject();
    obj->setProperty ("prompt", prompt);
    obj->setProperty ("session_id", sessionId);

    auto jsonBody = juce::JSON::toString (juce::var (obj.get()));
    auto response = doPost ("/generate", jsonBody, text2midi::kGenerateTimeoutMs);

    if (response.isEmpty())
        return {};

    return juce::JSON::parse (response);
}

bool HttpClient::configure (const juce::String& provider,
                             const juce::String& apiKey,
                             const juce::String& endpoint,
                             const juce::String& model)
{
    juce::DynamicObject::Ptr obj = new juce::DynamicObject();
    obj->setProperty ("provider", provider);
    obj->setProperty ("api_key", apiKey);
    obj->setProperty ("endpoint", endpoint);
    obj->setProperty ("model", model);

    auto jsonBody = juce::JSON::toString (juce::var (obj.get()));
    auto response = doPost ("/configure", jsonBody, text2midi::kConfigureTimeoutMs);

    if (response.isEmpty())
        return false;

    auto json = juce::JSON::parse (response);
    return json.getProperty ("status", "").toString() == "configured";
}
