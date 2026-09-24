import { appConfig } from "@/config/app";

const STORAGE_KEY = "app_settings";

export interface AppSettings {
  openaiApiKey: string;
  appName: string;
  appTagline: string;
  appVersion: string;
  appChannel: string;
}

const defaults: AppSettings = {
  openaiApiKey: "",
  appName: appConfig.name,
  appTagline: appConfig.tagline,
  appVersion: appConfig.version,
  appChannel: appConfig.channel,
};

function load(): AppSettings {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? { ...defaults, ...JSON.parse(raw) } : { ...defaults };
  } catch {
    return { ...defaults };
  }
}

export function getSettings(): AppSettings {
  return load();
}

export function saveSettings(settings: AppSettings): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
}
