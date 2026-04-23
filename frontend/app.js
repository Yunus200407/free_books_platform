// If frontend runs on :80 and backend on :8000 (common docker/local setup),
// same-origin calls would hit nginx instead of FastAPI.
const API_BASE = (window.location.port === '8000')
    ? window.location.origin
    : `${window.location.protocol}//${window.location.hostname}:8000`;

// DOM Elements
const booksGrid = document.getElementById('books-grid');
const addBookBtn = document.getElementById('add-book-btn');
const modal = document.getElementById('add-book-modal');
const closeBtn = document.querySelector('.close-btn');
const addBookForm = document.getElementById('add-book-form');

// State
let books = [];

// Fetch and display books
async function fetchBooks() {
    try {
        const response = await fetch(`${API_BASE}/books/`);
        if (!response.ok) throw new Error('Failed to fetch books');
        
        books = await response.json();
        renderBooks();
    } catch (error) {
        console.error('Error fetching books:', error);
        booksGrid.innerHTML = `<div class="loader" style="color: var(--danger-color)">Failed to load books. Please check server connection.</div>`;
    }
}

// Render books to the grid
function renderBooks() {
    if (books.length === 0) {
        booksGrid.innerHTML = '<div class="loader">No books available yet. Add some!</div>';
        return;
    }

    booksGrid.innerHTML = books.map(book => `
        <div class="book-card">
            <h3 class="book-title">${escapeHTML(book.title)}</h3>
            <div class="book-author">by ${escapeHTML(book.author)}</div>
            <div class="book-genre">${escapeHTML(book.genre)}</div>
            
            <div class="book-footer">
                <div class="download-count">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                    ${book.download_count}
                </div>
                <a href="${API_BASE}/download/${book.id}" target="_blank" class="download-btn" onclick="setTimeout(fetchBooks, 1000)">
                    Download
                </a>
            </div>
        </div>
    `).join('');
}

// Add a new book
async function addBook(event) {
    event.preventDefault();
    
    const submitBtn = addBookForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Adding...';
    submitBtn.disabled = true;

    const newBook = {
        title: document.getElementById('title').value,
        author: document.getElementById('author').value,
        genre: document.getElementById('genre').value,
        file_path: document.getElementById('file_path').value
    };

    try {
        const response = await fetch(`${API_BASE}/books/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newBook)
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Failed to add book');
        }

        // Reset form and close modal
        addBookForm.reset();
        closeModal();
        
        // Refresh book list
        await fetchBooks();
    } catch (error) {
        console.error('Error adding book:', error);
        alert(error.message);
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

// Modal logic
function openModal() {
    modal.classList.add('active');
}

function closeModal() {
    modal.classList.remove('active');
}

// Event Listeners
addBookBtn.addEventListener('click', openModal);
closeBtn.addEventListener('click', closeModal);
modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
});
addBookForm.addEventListener('submit', addBook);

// Helper function to prevent XSS
function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag])
    );
}

// Initial fetch
fetchBooks();
