document.addEventListener('DOMContentLoaded', function() {
    initializeProducts();
    
    setupEventListeners();
});

function initializeProducts() {
    const productsGrid = document.getElementById('productsGrid');
    
    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        productCard.innerHTML = `
            <img src="${product.image}" alt="${product.name}" class="product-image">
            <h3 class="product-title">${product.name}</h3>
            <p class="product-description">${product.description}</p>
            <div class="product-price">${product.price} руб.</div>
            <button class="add-to-cart" onclick="cart.addItem(${JSON.stringify(product).replace(/"/g, '&quot;')})">
                Добавить в корзину
            </button>
        `;
        productsGrid.appendChild(productCard);
    });
}

function setupEventListeners() {
    const cartButton = document.getElementById('cartButton');
    const closeCart = document.getElementById('closeCart');
    const cartSidebar = document.getElementById('cartSidebar');
    const checkoutButton = document.getElementById('checkoutButton');
    const modalOverlay = document.getElementById('modalOverlay');
    const closeModal = document.getElementById('closeModal');
    const orderForm = document.getElementById('orderForm');

    cartButton.addEventListener('click', () => {
        cartSidebar.classList.add('active');
    });

    closeCart.addEventListener('click', () => {
        cartSidebar.classList.remove('active');
    });

    checkoutButton.addEventListener('click', () => {
        if (cart.getTotalCount() === 0) {
            alert('Корзина пуста!');
            return;
        }
        cartSidebar.classList.remove('active');
        modalOverlay.classList.add('active');
    });

    closeModal.addEventListener('click', () => {
        modalOverlay.classList.remove('active');
    });

    
    orderForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        alert('Заказ создан!');
        
        cart.clearCart();
        orderForm.reset();
        modalOverlay.classList.remove('active');
    });

    modalOverlay.addEventListener('click', function(e) {
        if (e.target === modalOverlay) {
            modalOverlay.classList.remove('active');
        }
    });

}
