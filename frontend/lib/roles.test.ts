import { describe, expect, it } from "vitest";
import { isAdminUser } from "@/lib/roles";
import type { AuthUser } from "@/lib/authTypes";

const admin: AuthUser = {
  sub: "1",
  workspace_slug: "fredyc",
  role: "admin",
};

const user: AuthUser = {
  sub: "2",
  workspace_slug: "alice",
  role: "user",
};

describe("isAdminUser", () => {
  it("treats dev mode as admin", () => {
    expect(isAdminUser(null, false)).toBe(true);
    expect(isAdminUser(user, false)).toBe(true);
  });

  it("checks role when SSO is enabled", () => {
    expect(isAdminUser(admin, true)).toBe(true);
    expect(isAdminUser(user, true)).toBe(false);
    expect(isAdminUser(null, true)).toBe(false);
  });
});
