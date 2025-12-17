const API_URL = window.location.origin; // Используем тот же домен

// Global state
let currentUser = null;
let currentTab = 'menuTab';
let isLoginMode = true; // true = вход, false = регистрация
let cart = []; // Корзина со товарами
let allMenuItems = []; // Все товары из меню

// Elements
const authSection = document.getElementById('authSection');
const appSection = document.getElementById('appSection');
const loginBtn = document.getElementById('doLogin');
const logoutBtn = document.getElementById('logoutBtn');
const loginForm = document.getElementById('loginForm');
const menuBtns = document.querySelectorAll('.menu-btn');

// Event Listeners
loginBtn.addEventListener('click', handleLogin);
logoutBtn.addEventListener('click', handleLogout);
menuBtns.forEach(btn => {
    btn.addEventListener('click', (e) => handleTabSwitch(e.target));
});

// Toggle between login and register
function toggleAuthMode() {
    isLoginMode = !isLoginMode;
    const form = document.getElementById('authForm');
    const title = document.querySelector('.auth-card h2');
    const roleGroup = document.getElementById('roleGroup');
    const toggleBtn = document.getElementById('toggleAuthBtn');
    const submitBtn = document.getElementById('doLogin');
    
    if (isLoginMode) {
        title.textContent = '🔐 Вход';
        roleGroup.classList.add('hidden');
        toggleBtn.textContent = 'Создать аккаунт';
        submitBtn.textContent = '🔐 Вход';
        document.getElementById('loginUser').placeholder = 'Введите логин';
    } else {
        title.textContent = '📝 Регистрация';
        roleGroup.classList.remove('hidden');
        toggleBtn.textContent = 'Уже есть аккаунт? Войти';
        submitBtn.textContent = '✅ Зарегистрироваться';
        document.getElementById('loginUser').placeholder = 'Выберите логин';
    }
    
    // Clear form
    form.reset();
}

// Functions
async function handleLogin() {
    const username = document.getElementById('loginUser').value;
    const password = document.getElementById('loginPass').value;
    const fullName = document.getElementById('loginName')?.value;
    const role = document.getElementById('loginRole')?.value;

    if (!username || !password) {
        alert('Пожалуйста, заполните все поля');
        return;
    }

    try {
        if (isLoginMode) {
            // Login
            const response = await fetch(`${API_URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert('❌ Ошибка входа: ' + (errorData.detail || 'Проверьте логин и пароль'));
                return;
            }

            const data = await response.json();
            currentUser = data;
            cart = []; // Очистим корзину при входе

            // Show app section, hide auth
            authSection.classList.add('hidden');
            appSection.classList.remove('hidden');

            // Update UI
            document.getElementById('userName').textContent = data.full_name;
            document.getElementById('userRole').textContent = getRoleText(data.role);

            // Show/hide features based on role
            const ordersMenuBtn = Array.from(document.querySelectorAll('.menu-btn')).find(btn => btn.getAttribute('data-tab') === 'ordersTab');
            const cartBtn = document.getElementById('cartMenuBtn');
            const employeesBtn = document.getElementById('employeesMenuBtn');
            
            if (data.role === 'admin') {
                // Admin sees: Menu, Tables, Orders, Employees
                if (ordersMenuBtn) ordersMenuBtn.classList.remove('hidden');
                employeesBtn.classList.remove('hidden');
                document.getElementById('statEmployeeCard').classList.remove('hidden');
                cartBtn.classList.add('hidden');
            } else if (data.role === 'waiter') {
                // Waiter sees: Menu, Tables, Orders
                if (ordersMenuBtn) ordersMenuBtn.classList.remove('hidden');
                employeesBtn.classList.add('hidden');
                cartBtn.classList.add('hidden');
            } else if (data.role === 'user') {
                // User sees: Menu, Tables, My Order (корзина)
                if (ordersMenuBtn) ordersMenuBtn.classList.add('hidden');
                employeesBtn.classList.add('hidden');
                cartBtn.classList.remove('hidden');
            }

            // Load initial data
            loadMenuItems();
            loadTables();
            
            if (data.role !== 'user') {
                loadOrders();
            }
            
            if (data.role === 'admin') {
                loadEmployees();
            }

            console.log('✅ Успешный вход:', data);
        } else {
            // Register
            if (!fullName || !role) {
                alert('Пожалуйста, заполните все поля');
                return;
            }

            const response = await fetch(`${API_URL}/api/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    full_name: fullName,
                    role: role
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert('❌ Ошибка регистрации: ' + (errorData.detail || 'Такой логин уже существует'));
                return;
            }

            alert('✅ Аккаунт успешно создан! Теперь войдите.');
            toggleAuthMode(); // Switch to login mode
            console.log('✅ Регистрация успешна');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Ошибка: ' + error.message);
    }
}

function handleLogout() {
    currentUser = null;
    cart = [];
    authSection.classList.remove('hidden');
    appSection.classList.add('hidden');
    document.getElementById('authForm').reset();
    isLoginMode = true;
    document.querySelector('.auth-card h2').textContent = '🔐 Вход';
    document.getElementById('roleGroup').classList.add('hidden');
    document.getElementById('doLogin').textContent = '🔐 Вход';
}

function handleTabSwitch(btn) {
    menuBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    const tabName = btn.getAttribute('data-tab');
    document.querySelectorAll('.tabpane').forEach(tab => {
        tab.classList.add('hidden');
    });
    document.getElementById(tabName).classList.remove('hidden');
    currentTab = tabName;
    
    // Загружаем корзину когда открыта
    if (tabName === 'cartTab') {
        loadCart();
    }
}

// Menu items
async function loadMenuItems() {
    try {
        const response = await fetch(`${API_URL}/api/menu/`);
        const items = await response.json();
        allMenuItems = items; // Сохраняем все товары
        
        const menuContent = document.getElementById('menuContent');
        menuContent.innerHTML = '';
        
        if (items.length === 0) {
            menuContent.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #999;">Нет доступных пунктов меню</p>';
            return;
        }
        
        items.forEach(item => {
            const itemEl = document.createElement('div');
            itemEl.className = 'item';
            
            let html = `
                <div class="name">${item.name}</div>
                <div class="desc">${item.description || 'Без описания'}</div>
                <div class="meta">₽${item.price.toFixed(2)}</div>
                <small style="color: #999; display: block; margin-bottom: 10px;">${item.category}</small>
            `;
            
            if (currentUser && currentUser.role === 'user') {
                // Правильно генерируем onclick с параметрами
                html += `<button class="btn btn-primary" style="font-size: 12px; padding: 8px;" onclick="addToCart(${item.id}, '${item.name.replace(/'/g, "\\'")}'m ${item.price.toFixed(2)})">📋 Добавить в мой заказ</button>`;
            }
            
            itemEl.innerHTML = html;
            menuContent.appendChild(itemEl);
        });
        
        document.getElementById('statOrders').textContent = items.length;
    } catch (error) {
        console.error('Error loading menu:', error);
        document.getElementById('menuContent').innerHTML = '<p style="color: red;">❌ Ошибка загрузки меню</p>';
    }
}

// Tables
async function loadTables() {
    try {
        const response = await fetch(`${API_URL}/api/tables/`);
        const tables = await response.json();
        
        const tablesGrid = document.getElementById('tablesGrid');
        tablesGrid.innerHTML = '';
        
        if (tables.length === 0) {
            tablesGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #999;">Нет столов</p>';
            return;
        }
        
        let occupied = 0;
        tables.forEach(table => {
            if (table.is_occupied) occupied++;
            
            const tableEl = document.createElement('div');
            tableEl.className = 'item';
            tableEl.style.borderTop = table.is_occupied ? '4px solid #e74c3c' : '4px solid #2ecc71';
            tableEl.innerHTML = `
                <div class="name">Стол №${table.table_number}</div>
                <div class="desc">Мест: ${table.seats}</div>
                <div class="meta" style="color: ${table.is_occupied ? '#e74c3c' : '#2ecc71'};">
                    ${table.is_occupied ? '🔴 Занят' : '🟢 Свободен'}
                </div>
            `;
            tablesGrid.appendChild(tableEl);
        });
        
        document.getElementById('statTables').textContent = occupied;
    } catch (error) {
        console.error('Error loading tables:', error);
    }
}

// Orders
async function loadOrders() {
    try {
        const response = await fetch(`${API_URL}/api/orders/`);
        const orders = await response.json();
        
        const ordersList = document.getElementById('ordersList');
        ordersList.innerHTML = '';
        
        if (orders.length === 0) {
            ordersList.innerHTML = '<p style="text-align: center; color: #999;">Нет заказов</p>';
            return;
        }
        
        let active = 0;
        orders.forEach(order => {
            if (order.status === 'pending' || order.status === 'confirmed' || order.status === 'ready') {
                active++;
            }
            
            const orderEl = document.createElement('div');
            orderEl.className = 'order';
            orderEl.innerHTML = `
                <div class="name">Заказ #${order.id} - Стол №${order.table_id}</div>
                <div class="meta">Статус: <strong>${getStatusText(order.status)}</strong></div>
                <div class="meta">Сумма: ₽${order.total_price.toFixed(2)}</div>
            `;
            orderEl.addEventListener('click', () => showOrderDetails(order));
            ordersList.appendChild(orderEl);
        });
        
        document.getElementById('statActive').textContent = active;
        document.getElementById('statOrders').textContent = orders.length;
    } catch (error) {
        console.error('Error loading orders:', error);
    }
}

// КОРЗИНА ТОВАРОВ
function addToCart(itemId, itemName, itemPrice) {
    console.log('addToCart called with:', itemId, itemName, itemPrice);
    
    // Находим товар в меню по ID
    const menuItem = allMenuItems.find(item => item.id === itemId);
    
    if (!menuItem) {
        console.error('Item not found in allMenuItems:', itemId);
        alert('❌ Товар не найден');
        return;
    }
    
    const existingItem = cart.find(item => item.id === itemId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: itemId,
            name: menuItem.name,
            price: menuItem.price,
            quantity: 1
        });
    }
    
    console.log('Cart updated:', cart);
    alert(`✅ "${menuItem.name}" добавлено в мой заказ!`);
    updateCartBadge();
}

function updateCartBadge() {
    const badge = document.getElementById('cartBadge');
    if (badge) {
        const count = cart.reduce((sum, item) => sum + item.quantity, 0);
        badge.textContent = count;
        if (count === 0) {
            badge.classList.add('hidden');
        } else {
            badge.classList.remove('hidden');
        }
    }
}

function loadCart() {
    const cartContent = document.getElementById('cartContent');
    
    if (cart.length === 0) {
        cartContent.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #999;">
                <p>📝 Ваш заказ пуст</p>
                <p>Добавьте блюда из меню</p>
            </div>
        `;
        return;
    }
    
    let total = 0;
    let html = '<div class="cart-items">';
    
    cart.forEach((item, index) => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        
        html += `
            <div class="cart-item">
                <div style="flex: 1;">
                    <strong>${item.name}</strong>
                    <p style="margin: 5px 0; color: #666; font-size: 14px;">
                        ₽${item.price} x ${item.quantity} = ₽${itemTotal.toFixed(2)}
                    </p>
                </div>
                <div style="display: flex; gap: 5px; align-items: center;">
                    <button class="btn btn-secondary" style="width: 30px; height: 30px; padding: 0;" onclick="changeQuantity(${index}, -1)">-</button>
                    <span style="min-width: 20px; text-align: center;">${item.quantity}</span>
                    <button class="btn btn-secondary" style="width: 30px; height: 30px; padding: 0;" onclick="changeQuantity(${index}, 1)">+</button>
                    <button class="btn btn-danger" style="width: 40px; height: 30px; padding: 0; margin-left: 10px;" onclick="removeFromCart(${index})">x</button>
                </div>
            </div>
        `;
    });
    
    html += `</div>`;
    html += `
        <div style="margin-top: 20px; padding: 20px; background: #f9f9f9; border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; font-size: 18px; font-weight: bold; margin-bottom: 15px;">
                <span>Итого:</span>
                <span>₽${total.toFixed(2)}</span>
            </div>
            <div class="form-group">
                <label>Выберите стол</label>
                <select id="orderTableSelect">
                    <option value="">Выберите стол</option>
                </select>
            </div>
            <button class="btn btn-primary" onclick="createOrder()">📋 Оформить заказ</button>
        </div>
    `;
    
    cartContent.innerHTML = html;
    
    // Заполним выбор столов
    loadTablesForOrder();
}

async function loadTablesForOrder() {
    try {
        const response = await fetch(`${API_URL}/api/tables/`);
        const tables = await response.json();
        const select = document.getElementById('orderTableSelect');
        
        if (!select) return;
        
        tables.forEach(table => {
            if (!table.is_occupied) {
                const option = document.createElement('option');
                option.value = table.id;
                option.textContent = `Стол №${table.table_number} (${table.seats} мест)`;
                select.appendChild(option);
            }
        });
    } catch (error) {
        console.error('Error loading tables for order:', error);
    }
}

function changeQuantity(index, delta) {
    cart[index].quantity += delta;
    
    if (cart[index].quantity <= 0) {
        removeFromCart(index);
    } else {
        loadCart();
        updateCartBadge();
    }
}

function removeFromCart(index) {
    const itemName = cart[index].name;
    cart.splice(index, 1);
    alert(`"${itemName}" удален из заказа`);
    loadCart();
    updateCartBadge();
}

async function createOrder() {
    const tableSelect = document.getElementById('orderTableSelect');
    const tableId = tableSelect.value;
    
    if (!tableId) {
        alert('Пожалуйста, выберите стол');
        return;
    }
    
    if (cart.length === 0) {
        alert('Заказ пуст');
        return;
    }
    
    // Просто симулируем сохранение заказа
    // Когда будет backend - переслать данные на сервер
    alert(`👋 Заказ со стола #${tableId} составлен!\n\nВаш заказ принят официантом.`);
    
    // Очистим корзину
    cart = [];
    updateCartBadge();
    loadCart();
    
    // Обновим данные
    loadTables();
}

// Employees
async function loadEmployees() {
    try {
        const response = await fetch(`${API_URL}/api/employees/`);
        const employees = await response.json();
        
        const tableBody = document.getElementById('employeesTableBody');
        tableBody.innerHTML = '';
        
        if (employees.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #999;">Нет сотрудников</td></tr>';
            return;
        }
        
        employees.forEach(emp => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${emp.id}</td>
                <td>${emp.username}</td>
                <td>${emp.full_name}</td>
                <td><span class="role-badge ${emp.role}">${getRoleText(emp.role)}</span></td>
                <td>
                    <div class="employee-actions">
                        <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 12px;" onclick="alert('Функция в разработке')">✏️ Изменить</button>
                        <button class="btn btn-danger" style="padding: 4px 8px; font-size: 12px;" onclick="alert('Функция в разработке')">🗑️ Удалить</button>
                    </div>
                </td>
            `;
            tableBody.appendChild(row);
        });
        
        document.getElementById('statEmployees').textContent = employees.length;
    } catch (error) {
        console.error('Error loading employees:', error);
    }
}

// Modal functions
function addEmployeeModal() {
    if (!currentUser || currentUser.role !== 'admin') {
        alert('❌ Только администраторы могут добавлять сотрудников');
        return;
    }
    
    document.getElementById('modalTitle').textContent = 'Добавить сотрудника';
    document.getElementById('employeeForm').reset();
    document.getElementById('employeeModal').classList.remove('hidden');
}

function closeEmployeeModal() {
    document.getElementById('employeeModal').classList.add('hidden');
}

function closeOrderModal() {
    document.getElementById('orderModal').classList.add('hidden');
}

async function saveEmployee() {
    const username = document.getElementById('empUsername').value;
    const name = document.getElementById('empName').value;
    const password = document.getElementById('empPassword').value;
    const role = document.getElementById('empRole').value;

    if (!username || !name || !password || !role) {
        alert('Пожалуйста, заполните все поля');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/employees/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                full_name: name,
                password: password,
                role: role
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert('❌ Ошибка при создании сотрудника: ' + (errorData.detail || 'Неизвестная ошибка'));
            return;
        }

        alert('✅ Сотрудник успешно создан');
        closeEmployeeModal();
        loadEmployees();
    } catch (error) {
        console.error('Error saving employee:', error);
        alert('❌ Ошибка при сохранении: ' + error.message);
    }
}

function showOrderDetails(order) {
    let itemsHtml = '<div style="margin-top: 10px;">';
    if (order.items && order.items.length > 0) {
        order.items.forEach(item => {
            itemsHtml += `
                <div style="padding: 8px; background: #f9f9f9; margin-bottom: 8px; border-radius: 4px;">
                    <strong>${item.name || 'Товар'}</strong><br>
                    Кол-во: ${item.quantity} × ₽${item.price.toFixed(2)}
                </div>
            `;
        });
    } else {
        itemsHtml += '<p style="color: #999;">Нет товаров в заказе</p>';
    }
    itemsHtml += '</div>';

    document.getElementById('orderDetails').innerHTML = `
        <div style="margin-bottom: 15px;">
            <h4>Заказ #${order.id}</h4>
            <p><strong>Стол:</strong> №${order.table_id}</p>
            <p><strong>Статус:</strong> ${getStatusText(order.status)}</p>
            <p><strong>Сумма:</strong> ₽${order.total_price.toFixed(2)}</p>
        </div>
        <h4>Товары:</h4>
        ${itemsHtml}
    `;
    
    document.getElementById('orderModal').classList.remove('hidden');
}

function getStatusText(status) {
    const statuses = {
        'pending': '⏳ Ожидание',
        'confirmed': '✅ Подтвержден',
        'ready': '🟢 Готово',
        'completed': '✔️ Завершен',
        'cancelled': '❌ Отменен'
    };
    return statuses[status] || status;
}

function getRoleText(role) {
    const roles = {
        'waiter': '👔 Официант',
        'user': '👤 Пользователь',
        'admin': '👨‍💼 Администратор'
    };
    return roles[role] || role;
}

// Auto-refresh data
setInterval(() => {
    if (currentUser && currentUser.role !== 'user') {
        loadOrders();
        loadTables();
    }
}, 5000);

// Initial load
window.addEventListener('DOMContentLoaded', () => {
    console.log('✅ App initialized');
});
