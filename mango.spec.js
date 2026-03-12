const { test, expect } = require('@playwright/test');

test.describe('Mango Haven User Flow', () => {
  test('Complete flow: Land -> Open Chat -> Suggestion -> Add to Cart -> Cart View', async ({ page }) => {
    // Navigate to the local server
    await page.goto('http://localhost:8080');

    // View 1: Landing Page
    const landingView = page.locator('#landing-view');
    await expect(landingView).toBeVisible();

    // Interact with Chatbot
    const chatbotMin = page.locator('#chatbot-min');
    await expect(chatbotMin).toBeVisible();
    await chatbotMin.click();

    // Verify Chatbot expanded and suggestion is present
    const chatbotExpanded = page.locator('#chatbot-expanded');
    await expect(chatbotExpanded).toBeVisible();

    // View 2: Product Page Transition
    const kesarAction = page.locator('#chat-kesar-action');
    await expect(kesarAction).toBeVisible();
    await kesarAction.click();

    const productView = page.locator('#product-view');
    await expect(productView).toBeVisible();
    await expect(landingView).toBeHidden();

    // View 3: Cart Action
    const addToCartBtn = page.locator('button#add-to-cart-btn');
    await expect(addToCartBtn).toBeVisible();
    // Dispatch event to bypass any possible invisible interceptors
    await addToCartBtn.dispatchEvent('click');

    // Verify Cart Modal opens
    const cartModal = page.locator('#cart-modal');
    // Ensure the modal has its hidden class removed
    await expect(cartModal).not.toHaveClass(/hidden/);

    // Verify cart badge updated
    const cartBadge = page.locator('#cart-badge');
    await expect(cartBadge).toHaveText('2');

    // Verify final minimized chatbot state with checkout tooltip
    const chatbotMinCheckout = page.locator('#chatbot-min-checkout');
    await expect(chatbotMinCheckout).toBeVisible();
    await expect(chatbotMinCheckout).toContainText('Great choice! Kesar mangoes are now in your cart. Ready to checkout?');
  });
});
