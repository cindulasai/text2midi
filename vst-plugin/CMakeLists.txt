cmake_minimum_required(VERSION 3.22)
project(text2midi VERSION 0.1.0)

add_subdirectory(libs/JUCE)

juce_add_plugin(text2midi
    COMPANY_NAME "text2midi"
    PLUGIN_MANUFACTURER_CODE Tx2M
    PLUGIN_CODE Tx2m
    FORMATS VST3
    PRODUCT_NAME "text2midi"
    IS_SYNTH TRUE
    NEEDS_MIDI_INPUT TRUE
    NEEDS_MIDI_OUTPUT FALSE
    IS_MIDI_EFFECT FALSE
    EDITOR_WANTS_KEYBOARD_FOCUS TRUE
    COPY_PLUGIN_AFTER_BUILD FALSE
)

target_sources(text2midi PRIVATE
    source/PluginProcessor.cpp
    source/PluginEditor.cpp
    source/ApiKeyPanel.cpp
    source/GenrePresetPanel.cpp
    source/PromptPanel.cpp
    source/OutputPanel.cpp
    source/DraggableMidiFile.cpp
    source/HttpClient.cpp
    source/ProgressPanel.cpp
    source/BackendLauncher.cpp
)

target_compile_definitions(text2midi PUBLIC
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=1
    JUCE_VST3_CAN_REPLACE_VST2=0
)

target_link_libraries(text2midi PRIVATE
    juce::juce_audio_utils
    juce::juce_gui_extra
    juce::juce_recommended_config_flags
    juce::juce_recommended_lto_flags
    juce::juce_recommended_warning_flags
)
