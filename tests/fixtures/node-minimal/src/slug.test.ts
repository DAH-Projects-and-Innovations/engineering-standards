import { describe, expect, it } from "vitest";

import { MAX_SLUG_LENGTH, slugify } from "./slug.js";

describe("slugify", () => {
  it("returns kebab-case for a simple title", () => {
    expect(slugify("Add Cohere embedder")).toBe("add-cohere-embedder");
  });

  it("removes accents", () => {
    expect(slugify("Données de santé")).toBe("donnees-de-sante");
  });

  it("limits the length without a trailing hyphen", () => {
    const slug = slugify("word ".repeat(30));
    expect(slug.length).toBeLessThanOrEqual(MAX_SLUG_LENGTH);
    expect(slug.endsWith("-")).toBe(false);
  });

  it("throws when nothing is left", () => {
    expect(() => slugify("!!!")).toThrow(RangeError);
  });
});
