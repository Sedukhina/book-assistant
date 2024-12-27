// books.js - Load + render books via fetch (no "genre" field)

document.addEventListener("DOMContentLoaded", () => {
  const resultsContainer = document.getElementById("resultsContainer");
  const noResultsMsg = document.getElementById("noResultsMsg");

  const btnSearch = document.getElementById("btnSearch");
  const btnApplyFilters = document.getElementById("btnApplyFilters");
  const searchTitle = document.getElementById("searchTitle");

  // Optionally load all books on initial page load:
  loadBooks();

  // The "Search" button (top bar) triggers a data fetch
  if (btnSearch) {
    btnSearch.addEventListener("click", () => {
      loadBooks();
    });
  }

  if (searchTitle) {
    searchTitle.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        loadBooks();
      }
    });
  }

  // The "Apply Filters" button (left side)
  if (btnApplyFilters) {
    btnApplyFilters.addEventListener("click", () => {
      loadBooks();
    });
  }

  async function loadBooks() {
    // Gather Title from top bar
    const title = (document.getElementById("searchTitle")?.value || "").trim();

    // Gather Author substring
    const author = (document.getElementById("author")?.value || "").trim();

    // Gather Categories (checkboxes)
    const catCheckboxes = document.querySelectorAll('input[name="categories"]:checked');
    const categories = Array.from(catCheckboxes).map(cb => cb.value);

    // Gather Year range
    const yearFrom = (document.getElementById("yearFrom")?.value || "").trim();
    const yearTo = (document.getElementById("yearTo")?.value || "").trim();

    // Build query params
    const params = new URLSearchParams();
    if (title) params.append("title", title);
    if (author) params.append("author", author);
    if (categories.length > 0) {
      params.append("categories", categories.join(","));
    }
    if (yearFrom) params.append("year_from", yearFrom);
    if (yearTo) params.append("year_to", yearTo);

    try {
      // Example: fetch from /api/books?title=...&author=... etc.
      const response = await fetch(`/api/books?${params.toString()}`);
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      const data = await response.json();
      renderBooks(data);
    } catch (err) {
      console.error("Error fetching books:", err);
      resultsContainer.innerHTML = `<p style="color:red;">Error loading data.</p>`;
    }
  }

  function renderBooks(books) {
    resultsContainer.innerHTML = ""; // clear old results

    if (!books || books.length === 0) {
      noResultsMsg.style.display = "block";
      return;
    }
    noResultsMsg.style.display = "none";

    books.forEach(book => {
      // Create a card
      const card = document.createElement("div");
      card.classList.add("grid-item", "book-card");

      // Cover
      const coverWrapper = document.createElement("div");
      coverWrapper.classList.add("cover-wrapper");
      const img = document.createElement("img");
      img.alt = `${book.title} cover`;
      // If your data has a "cover" property, use it; otherwise placeholder
      if (book.cover) {
        img.src = `/static/img/covers/${book.cover}`;
      } else {
        img.src = `/static/img/bookCover.png`;
      }
      coverWrapper.appendChild(img);
      card.appendChild(coverWrapper);

      // Info
      const infoDiv = document.createElement("div");
      infoDiv.classList.add("book-info");

      // Title
      const titleEl = document.createElement("h3");
      titleEl.classList.add("book-title");
      titleEl.textContent = book.title;
      infoDiv.appendChild(titleEl);

      // Author
      const authorEl = document.createElement("p");
      authorEl.classList.add("book-author");
      authorEl.textContent = `By: ${book.author}`;
      infoDiv.appendChild(authorEl);

      // Categories
      if (book.categories && book.categories.length > 0) {
        const catEl = document.createElement("p");
        catEl.classList.add("book-categories");
        catEl.innerHTML = `<strong>Categories:</strong> ${book.categories.join(", ")}`;
        infoDiv.appendChild(catEl);
      }

      // Publish Year
      if (book.publishDate) {
        const yearEl = document.createElement("p");
        yearEl.classList.add("book-year");
        yearEl.innerHTML = `<strong>Published:</strong> ${book.publishDate}`;
        infoDiv.appendChild(yearEl);
      }

      card.appendChild(infoDiv);
      resultsContainer.appendChild(card);
    });
  }
});
