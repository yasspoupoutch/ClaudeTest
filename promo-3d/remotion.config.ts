import { Config } from '@remotion/cli/config';
// Headless Chromium from this machine, software WebGL through ANGLE/SwiftShader.
Config.setBrowserExecutable('/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell');
Config.setChromiumOpenGlRenderer('swangle');
Config.setVideoImageFormat('png');
Config.setDelayRenderTimeoutInMilliseconds(120000);
