/**
 * Library Inventory — Frontend Controller
 * Connects UI to Flask REST API (/api/items)
 */

document.addEventListener('DOMContentLoaded', () => {
  // --- DOM Elements ---
  const notificationArea = document.getElementById('notification-area');
  const notificationTitle = document.getElementById('notification-title');
  const notificationMessage = document.getElementById('notification-message');
  const notificationClose = document.getElementById('notification-close');

  const itemForm = document.getElementById('item-form');
  const formSectionTag = document.getElementById('form-section-tag');
  const formTitle = document.getElementById('form-title');
  const formDesc = document.getElementById('form-desc');
  const editItemIdInput = document.getElementById('edit-item-id');
  const itemTitleInput = document.getElementById('item-title');
  const itemAuthorInput = document.getElementById('item-author');
  const itemMetricInput = document.getElementById('item-metric');
  const metricLabel = document.getElementById('metric-label');
  const metricSuffix = document.getElementById('metric-suffix');
  const submitBtnText = document.getElementById('submit-btn-text');
  const cancelEditBtn = document.getElementById('cancel-edit-btn');
  const typeSelector = document.getElementById('type-selector');
  const typeGroup = document.getElementById('type-group');

  const itemsListContainer = document.getElementById('items-list');
  const itemCountSpan = document.getElementById('item-count');
  const filterTabs = document.querySelectorAll('.filter-tab');
  const availableToggle = document.getElementById('available-toggle');

  // --- State ---
  let selectedType = 'book';
  let activeFilterType = 'all';
  let filterAvailableOnly = false;
  let notificationTimer = null;

  // --- Notification / Error Area (Requirement #2) ---
  function showNotification(title, message, isError = true) {
    if (notificationTimer) clearTimeout(notificationTimer);

    notificationArea.className = `notification-area ${isError ? 'error' : 'success'}`;
    const icon = isError ? '⚠️' : '✅';
    document.getElementById('notification-icon').textContent = icon;
    notificationTitle.textContent = title;
    notificationMessage.textContent = message;
    notificationArea.style.display = 'flex';

    // Auto-dismiss after 6 seconds
    notificationTimer = setTimeout(() => {
      hideNotification();
    }, 6000);
  }

  function hideNotification() {
    notificationArea.style.display = 'none';
    if (notificationTimer) clearTimeout(notificationTimer);
  }

  notificationClose.addEventListener('click', hideNotification);

  // --- Form Type Selection (Book vs DVD) ---
  typeSelector.querySelectorAll('.segment').forEach(btn => {
    btn.addEventListener('click', () => {
      typeSelector.querySelectorAll('.segment').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedType = btn.dataset.type;
      updateMetricLabels();
    });
  });

  function updateMetricLabels() {
    if (selectedType === 'book') {
      metricLabel.textContent = 'Page count';
      metricSuffix.textContent = 'pages';
      itemMetricInput.placeholder = '320';
    } else {
      metricLabel.textContent = 'Duration';
      metricSuffix.textContent = 'mins';
      itemMetricInput.placeholder = '120';
    }
  }

  // --- Fetch & Render Items from REST API ---
  async function fetchItems() {
    try {
      const params = new URLSearchParams();
      if (filterAvailableOnly) {
        params.append('available', 'true');
      }
      if (activeFilterType !== 'all') {
        params.append('type', activeFilterType);
      }

      const queryString = params.toString() ? `?${params.toString()}` : '';
      const response = await fetch(`/api/items${queryString}`);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        showNotification(`Error ${response.status}`, errorData.error || 'Failed to fetch items');
        return;
      }

      const items = await response.json();
      renderItems(items);
    } catch (err) {
      showNotification('Network Error', 'Could not connect to Flask server. Please make sure the app is running.');
    }
  }

  function renderItems(items) {
    itemCountSpan.textContent = items.length;

    if (items.length === 0) {
      itemsListContainer.innerHTML = `
        <div class="empty-state">
          No items found matching the current filters.
        </div>
      `;
      return;
    }

    itemsListContainer.innerHTML = items.map(item => {
      const isBook = item.type.toLowerCase() === 'book';
      const metricText = isBook ? `${item.page_count} pages` : `${item.duration} min`;
      const statusPill = item.is_available
        ? `<div class="status-pill available"><span class="dot"></span> Available</div>`
        : `<div class="status-pill checked-out"><span class="dot"></span> Checked out</div>`;

      const actionButton = item.is_available
        ? `<button class="btn-action btn-checkout" data-action="checkout" data-id="${item.id}">Checkout</button>`
        : `<button class="btn-action btn-return" data-action="return" data-id="${item.id}">Return</button>`;

      const thumbIcon = isBook
        ? `<svg class="thumb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
             <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
             <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
           </svg>`
        : `<svg class="thumb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
             <circle cx="12" cy="12" r="10"></circle>
             <circle cx="12" cy="12" r="3"></circle>
           </svg>`;

      return `
        <div class="item-card" data-id="${item.id}">
          <div class="item-thumb ${isBook ? 'book-thumb' : 'dvd-thumb'}">
            ${thumbIcon}
          </div>
          
          <div class="item-info">
            <h3 class="item-title">${escapeHtml(item.title)}</h3>
            <div class="item-author">by ${escapeHtml(item.author)}</div>
            <div class="item-meta">${item.type} • ${metricText}</div>
          </div>

          ${statusPill}

          <div class="item-actions">
            ${actionButton}
            <button class="btn-icon btn-edit" title="Edit Item" data-action="edit" data-id="${item.id}">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 20h9"></path>
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
              </svg>
            </button>
            <button class="btn-icon btn-delete" title="Delete Item" data-action="delete" data-id="${item.id}">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
          </div>
        </div>
      `;
    }).join('');
  }

  // --- Handle Card Actions: Checkout, Return, Delete, Edit ---
  itemsListContainer.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;

    const action = btn.dataset.action;
    const itemId = btn.dataset.id;

    if (action === 'checkout') {
      await handleCheckout(itemId);
    } else if (action === 'return') {
      await handleReturn(itemId);
    } else if (action === 'delete') {
      await handleDelete(itemId);
    } else if (action === 'edit') {
      await enterEditMode(itemId);
    }
  });

  // --- Checkout Item ---
  async function handleCheckout(itemId) {
    try {
      const response = await fetch(`/api/items/${itemId}/checkout`, {
        method: 'POST'
      });
      const data = await response.json();

      if (response.ok) {
        showNotification('Checked Out', data.message || 'Item checked out successfully.', false);
        fetchItems();
      } else {
        // e.g. 409 Already checked out
        showNotification(`Error ${response.status}`, data.error || 'Checkout failed');
      }
    } catch (err) {
      showNotification('Network Error', 'Failed to communicate with API.');
    }
  }

  // --- Return Item ---
  async function handleReturn(itemId) {
    try {
      const response = await fetch(`/api/items/${itemId}/return`, {
        method: 'POST'
      });
      const data = await response.json();

      if (response.ok) {
        showNotification('Returned', data.message || 'Item returned successfully.', false);
        fetchItems();
      } else {
        // e.g. 409 Not checked out
        showNotification(`Error ${response.status}`, data.error || 'Return failed');
      }
    } catch (err) {
      showNotification('Network Error', 'Failed to communicate with API.');
    }
  }

  // --- Delete Item (Crucial 409 Error Requirement) ---
  async function handleDelete(itemId) {
    try {
      const response = await fetch(`/api/items/${itemId}`, {
        method: 'DELETE'
      });

      if (response.status === 204) {
        showNotification('Deleted', `Item #${itemId} was deleted from the library.`, false);
        fetchItems();
      } else {
        const data = await response.json().catch(() => ({}));
        // Shows 409 Conflict if item is checked out!
        showNotification(`Error ${response.status}`, data.error || 'Cannot delete item');
      }
    } catch (err) {
      showNotification('Network Error', 'Failed to communicate with API.');
    }
  }

  // --- Edit Item Mode ---
  async function enterEditMode(itemId) {
    try {
      const response = await fetch(`/api/items/${itemId}`);
      if (!response.ok) {
        const data = await response.json();
        showNotification(`Error ${response.status}`, data.error);
        return;
      }

      const item = await response.json();
      editItemIdInput.value = item.id;
      itemTitleInput.value = item.title;
      itemAuthorInput.value = item.author;

      const isBook = item.type.toLowerCase() === 'book';
      selectedType = isBook ? 'book' : 'dvd';
      itemMetricInput.value = isBook ? item.page_count : item.duration;

      // Lock type in edit mode
      typeGroup.style.display = 'none';
      updateMetricLabels();

      formSectionTag.textContent = `EDIT RECORD #${item.id}`;
      formTitle.textContent = 'Edit item';
      formDesc.textContent = 'Update the details for this item in the collection.';
      submitBtnText.textContent = 'Save changes';
      cancelEditBtn.style.display = 'inline-flex';

      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      showNotification('Error', 'Could not load item details for editing.');
    }
  }

  function exitEditMode() {
    editItemIdInput.value = '';
    itemForm.reset();
    typeGroup.style.display = 'block';
    selectedType = 'book';
    typeSelector.querySelectorAll('.segment').forEach(b => {
      b.classList.toggle('active', b.dataset.type === 'book');
    });
    updateMetricLabels();

    formSectionTag.textContent = 'NEW RECORD';
    formTitle.textContent = 'Add an item';
    formDesc.textContent = 'Enter the details below to add it to the collection.';
    submitBtnText.textContent = 'Add to library';
    cancelEditBtn.style.display = 'none';
  }

  cancelEditBtn.addEventListener('click', exitEditMode);

  // --- Add or Update Item Submit Handler ---
  itemForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const title = itemTitleInput.value.trim();
    const author = itemAuthorInput.value.trim();
    const metricVal = parseInt(itemMetricInput.value, 10);
    const editingId = editItemIdInput.value;

    if (!title || !author || isNaN(metricVal)) {
      showNotification('Validation Error', 'Please fill in all required fields.');
      return;
    }

    if (editingId) {
      // PUT /api/items/<id> (Update)
      const payload = {
        title,
        author,
        ...(selectedType === 'book' ? { page_count: metricVal } : { duration: metricVal })
      };

      try {
        const response = await fetch(`/api/items/${editingId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (response.ok) {
          showNotification('Updated', `Item "${title}" was updated successfully.`, false);
          exitEditMode();
          fetchItems();
        } else {
          showNotification(`Error ${response.status}`, data.error || 'Failed to update item');
        }
      } catch (err) {
        showNotification('Network Error', 'Failed to save changes.');
      }

    } else {
      // POST /api/items (Create)
      const payload = {
        type: selectedType,
        title,
        author,
        ...(selectedType === 'book' ? { page_count: metricVal } : { duration: metricVal })
      };

      try {
        const response = await fetch('/api/items', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (response.status === 201) {
          showNotification('Added', `"${title}" was added to the library collection.`, false);
          itemForm.reset();
          fetchItems();
        } else {
          showNotification(`Error ${response.status}`, data.error || 'Failed to add item');
        }
      } catch (err) {
        showNotification('Network Error', 'Failed to add item to API.');
      }
    }
  });

  // --- Filter Tabs (All, Book, DVD) ---
  filterTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      filterTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      activeFilterType = tab.dataset.filterType;
      fetchItems();
    });
  });

  // --- Available Only Toggle ---
  availableToggle.addEventListener('change', () => {
    filterAvailableOnly = availableToggle.checked;
    fetchItems();
  });

  // --- Utility ---
  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>"']/g, match => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    }[match]));
  }

  // --- Initial Load ---
  fetchItems();
});
