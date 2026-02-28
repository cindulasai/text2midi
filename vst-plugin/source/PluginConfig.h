/*
  ==============================================================================
    PluginConfig.h
    text2midi VST3 Plugin — Global constants
  ==============================================================================
*/

#pragma once

namespace text2midi
{

// ── Backend Server ──────────────────────────────────────────────────────────
inline constexpr const char* kBackendHost       = "127.0.0.1";
inline constexpr int         kBackendPort       = 18323;
inline constexpr const char* kBackendBaseUrl    = "http://127.0.0.1:18323";
inline constexpr const char* kServerExeName     = "text2midi-backend.exe";

// ── HTTP Timeouts (ms) ─────────────────────────────────────────────────────
inline constexpr int kHealthTimeoutMs           = 2000;
inline constexpr int kConfigureTimeoutMs        = 5000;
inline constexpr int kGenerateTimeoutMs         = 60000;

// ── Backend Launch ──────────────────────────────────────────────────────────
inline constexpr int kBackendLaunchTimeoutMs    = 10000;
inline constexpr int kBackendPollIntervalMs     = 500;

// ── Plugin UI ───────────────────────────────────────────────────────────────
inline constexpr int kPluginWidth               = 620;
inline constexpr int kPluginHeight              = 800;

// ── Pipeline Nodes ──────────────────────────────────────────────────────────
inline constexpr int kTotalNodes                = 8;

// ── Colours (Catppuccin Mocha) ──────────────────────────────────────────────
inline constexpr unsigned int kColBase          = 0xFF1E1E2E;
inline constexpr unsigned int kColSurface0      = 0xFF313244;
inline constexpr unsigned int kColSurface1      = 0xFF45475A;
inline constexpr unsigned int kColSurface2      = 0xFF585B70;
inline constexpr unsigned int kColOverlay0      = 0xFF6C7086;
inline constexpr unsigned int kColText          = 0xFFCDD6F4;
inline constexpr unsigned int kColSubtext       = 0xFFA6ADC8;
inline constexpr unsigned int kColBlue          = 0xFF89B4FA;
inline constexpr unsigned int kColGreen         = 0xFFA6E3A1;
inline constexpr unsigned int kColRed           = 0xFFF38BA8;
inline constexpr unsigned int kColYellow        = 0xFFF9E2AF;
inline constexpr unsigned int kColPeach         = 0xFFFAB387;
inline constexpr unsigned int kColMauve         = 0xFFCBA6F7;

// ── Version ─────────────────────────────────────────────────────────────────
inline constexpr const char* kPluginVersion     = "0.1.0";

} // namespace text2midi
