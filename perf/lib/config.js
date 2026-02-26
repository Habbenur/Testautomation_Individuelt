export const BASE_URL = ( (__ENV.BASE_URL || "https://kzmcpfklrqymzazaxlmv.supabase.co/functions/v1") ).replace(/\/$/, "");

export const X_API_KEY = __ENV.X_API_KEY;
export const X_ADMIN_API_KEY = __ENV.X_ADMIN_API_KEY;

export function assertConfig() {
  if (!X_API_KEY) throw new Error("Missing env var: X_API_KEY");
  if (!X_ADMIN_API_KEY) throw new Error("Missing env var: X_ADMIN_API_KEY");
}