/** Maximum length of a slug, in characters. */
export const MAX_SLUG_LENGTH = 60;

/**
 * Turn a title into a URL-friendly slug, for example a branch description.
 *
 * @param title - Free text, for example "Add Cohere embedder".
 * @returns The slug in kebab-case, for example "add-cohere-embedder".
 * @throws {RangeError} If the title contains no letter or digit.
 */
export function slugify(title: string): string {
  const slug = title
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, MAX_SLUG_LENGTH)
    .replace(/-+$/g, "");
  if (slug === "") {
    throw new RangeError(`Cannot build a slug from ${JSON.stringify(title)}`);
  }
  return slug;
}
