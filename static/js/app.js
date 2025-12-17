const API_URL = 'http://localhost:8000';

// Global state
let currentUser = null;
let currentTab = 'menuTab';

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

// Functions
async function handleLogin() {
    const username = document.getElementById('loginUser').value;
    const password = document.getElementById('loginPass').value;

    if (!username || !password) {
        alert('Пожалуйста, заполните все поля');
        return;
    }

    try {
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
            alert('Ошибка входа. Проверьте логин и пароль');
            return;
        }

        const data = await response.json();
        currentUser = data;

        // Show app section, hide auth
        authSection.classList.add('hidden');
        appSection.classList.remove('hidden');

        // Update UI
        document.getElementById('userName').textContent = data.full_name;
        document.getElementById('userRole').textContent = data.role;

        // Show admin-only features
        if (data.role === 'admin') {
            document.getElementById('employeesMenuBtn').classList.remove('hidden');
            document.getElementById('statEmployeeCard').classList.remove('hidden');
        }

        // Load initial data
        loadMenuItems();
        loadTables();
        loadOrders();
        if (data.role === 'admin') {
            loadEmployees();
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Ошибка при входе');
    }
}

function handleLogout() {
    currentUser = null;
    authSection.classList.remove('hidden');
    appSection.classList.add('hidden');
    document.getElementById('loginForm').reset();
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
}

// Menu items
async function loadMenuItems() {
    try {
        const response = await fetch(`${API_URL}/api/menu/`);
        const items = await response.json();
        
        const menuContent = document.getElementById('menuContent');
        menuContent.innerHTML = '';
        
        items.forEach(item => {
            const itemEl = document.createElement('div');
            itemEl.className = 'item';
            itemEl.innerHTML = `
                <div class="name">${item.name}</div>
                <div class="desc">${item.description || 'Без описания'}</div>
                <div class="meta">₽${item.price}</div>
                <small style="color: #999;">${item.category}</small>
            `;
            menuContent.appendChild(itemEl);
        });
        
        document.getElementById('statOrders').textContent = items.length;
    } catch (error) {
        console.error('Error loading menu:', error);
    }
}

// Tables
async function loadTables() {
    try {
        const response = await fetch(`${API_URL}/api/tables/`);
        const tables = await response.json();
        
        const tablesGrid = document.getElementById('tablesGrid');
        tablesGrid.innerHTML = '';
        
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
                <div class="meta">Сумма: ₽${order.total_price}</div>
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

// Employees
async function loadEmployees() {
    try {
        const response = await fetch(`${API_URL}/api/employees/`);
        const employees = await response.json();
        
        const tableBody = document.getElementById('employeesTableBody');
        tableBody.innerHTML = '';
        
        employees.forEach(emp => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${emp.id}</td>
                <td>${emp.username}</td>
                <td>${emp.full_name}</td>
                <td><span class="role-badge ${emp.role}">${getRoleText(emp.role)}</span></td>
                <td>
                    <div class="employee-actions">
                        <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 12px;">Изменить</button>
                        <button class="btn btn-danger" style="padding: 4px 8px; font-size: 12px;">Удалить</button>
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
            alert('Ошибка при создании сотрудника');
            return;
        }

        alert('Сотрудник успешно создан');
        closeEmployeeModal();
        loadEmployees();
    } catch (error) {
        console.error('Error saving employee:', error);
        alert('Ошибка при сохранении');
    }
}

function showOrderDetails(order) {
    let itemsHtml = '<div style="margin-top: 10px;">';
    order.items.forEach(item => {
        itemsHtml += `
            <div style="padding: 8px; background: #f9f9f9; margin-bottom: 8px; border-radius: 4px;">
                <strong>${item.name}</strong><br>
                Кол-во: ${item.quantity} × ₽${item.price}
            </div>
        `;
    });
    itemsHtml += '</div>';

    document.getElementById('orderDetails').innerHTML = `
        <div style="margin-bottom: 15px;">
            <h4>Заказ #${order.id}</h4>
            <p><strong>Стол:</strong> №${order.table_id}</p>
            <p><strong>Статус:</strong> ${getStatusText(order.status)}</p>
            <p><strong>Сумма:</strong> ₽${order.total_price}</p>
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
        'waiter': 'Официант',
        'chef': 'Повар',
        'admin': 'Админ'
    };
    return roles[role] || role;
}

// Auto-refresh data
setInterval(() => {
    if (currentUser) {
        loadOrders();
        loadTables();
    }
}, 5000);
