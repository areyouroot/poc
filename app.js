// app.js

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatbotMin = document.getElementById('chatbot-min');
    const chatbotExpanded = document.getElementById('chatbot-expanded');
    const closeChatbotBtn = document.getElementById('close-chatbot-btn');
    const chatKesarAction = document.getElementById('chat-kesar-action');

    const landingView = document.getElementById('landing-view');
    const productView = document.getElementById('product-view');

    const addToCartBtn = document.getElementById('add-to-cart-btn');
    const headerCartBtn = document.getElementById('header-cart-btn');
    const cartBadge = document.getElementById('cart-badge');

    const cartModal = document.getElementById('cart-modal');
    const closeCartBtn = document.getElementById('close-cart-btn');
    const cartOverlay = document.getElementById('cart-overlay');

    const chatbotMinCheckout = document.getElementById('chatbot-min-checkout');

    // 1. Initial State: Click chatbot on landing page to expand it
    chatbotMin.addEventListener('click', () => {
        chatbotMin.classList.add('hidden');
        chatbotExpanded.classList.remove('hidden');
    });

    // Close chatbot manually
    closeChatbotBtn.addEventListener('click', () => {
        chatbotExpanded.classList.add('hidden');
        chatbotMin.classList.remove('hidden');
    });

    // 2. Click "Yes, show me Kesar offers!" in the chat
    chatKesarAction.addEventListener('click', () => {
        // Transition from landing page to product page
        landingView.classList.add('hidden');
        productView.classList.remove('hidden');
    });

    // 3. Click "Add Kesar to Cart" on the product page
    addToCartBtn.addEventListener('click', (e) => {
        e.preventDefault();
        // Update cart badge
        cartBadge.textContent = '2';

        // Hide expanded chatbot
        chatbotExpanded.classList.add('hidden');

        // Open Cart Modal
        openCart();

        // Show the new checkout state chatbot
        chatbotMinCheckout.classList.remove('hidden');
    });

    // Cart Modal Logic
    const openCart = () => {
        cartModal.classList.remove('hidden');
        cartOverlay.classList.remove('hidden');
        // Small delay to allow display block to apply before animating transform
        setTimeout(() => {
            cartModal.classList.remove('translate-x-full');
        }, 50);
    };

    const closeCart = () => {
        cartModal.classList.add('translate-x-full');
        cartOverlay.classList.add('hidden');
        // Hide after animation finishes
        setTimeout(() => {
            cartModal.classList.add('hidden');
        }, 300);
    };

    // Open cart from header icon
    headerCartBtn.addEventListener('click', openCart);

    // Close cart actions
    closeCartBtn.addEventListener('click', closeCart);
    cartOverlay.addEventListener('click', closeCart);
});
