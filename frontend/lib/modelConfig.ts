/** Shared model catalog + config helpers for Settings and chat switcher. */

export type CatalogModel = {
  id: string;
  display_name: string;
  api_base: string;
  provider_type: string;
  api_version?: string | null;
  api_model?: string | null;
  api_key?: string;
  has_api_key: boolean;
  temperature: number;
  max_tokens: number;
};

export type ModelCatalog = {
  provider_id: string;
  provider_name: string;
  description: string;
  default_model: string;
  defaults: { temperature: number; max_tokens: number };
  models: CatalogModel[];
};

export type UserModelConfig = {
  provider: string;
  model: string;
  api_key: string;
  base_url: string;
  temperature: number;
  api_version?: string;
  api_model?: string;
  max_tokens?: number | null;
  api_key_set?: boolean;
};

export type UserConfig = {
  model: UserModelConfig;
  system_prompt: string;
  approve_writes: boolean;
  approve_execute: boolean;
  enabled_tools: Record<string, boolean>;
  permissions: unknown[];
};

export function applyCatalogModel(
  cfg: UserConfig,
  catalog: ModelCatalog,
  modelId: string
): UserConfig {
  const m = catalog.models.find((x) => x.id === modelId);
  if (!m) {
    return { ...cfg, model: { ...cfg.model, model: modelId } };
  }
  return {
    ...cfg,
    model: {
      ...cfg.model,
      provider: catalog.provider_id,
      model: m.id,
      base_url: m.api_base,
      api_key: m.api_key || cfg.model.api_key,
      api_version: m.api_version || "",
      api_model: m.api_model || "",
      temperature: m.temperature ?? catalog.defaults.temperature,
      max_tokens: m.max_tokens ?? catalog.defaults.max_tokens,
      api_key_set: Boolean(m.api_key || cfg.model.api_key_set),
    },
  };
}

export function catalogLabel(catalog: ModelCatalog | null, modelId: string): string {
  const found = catalog?.models.find((m) => m.id === modelId);
  return found?.display_name || modelId;
}
