// DAH Labs Vitest configuration template (rule JS-006).
// For React components add: environment "jsdom" and @testing-library/react.
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["src/**/*.test.{ts,tsx}", "tests/**/*.test.{ts,tsx}"],
    // environment: "jsdom", // TODO: uncomment for React components.
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov"], // lcov.info is read by SonarQube Cloud.
      include: ["src/**"],
    },
  },
});
