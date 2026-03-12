const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './',
  use: {
    headless: true,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
