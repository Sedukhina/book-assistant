// books.js - Load + render books via fetch (no "genre" field)

document.addEventListener("DOMContentLoaded", () => {
  const resultsContainer = document.getElementById("resultsContainer");
  const noResultsMsg = document.getElementById("noResultsMsg");

  const btnSearch = document.getElementById("btnSearch");
  const btnApplyFilters = document.getElementById("btnApplyFilters");
  const searchTitle = document.getElementById("searchTitle");

  loadBooks();

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

  if (btnApplyFilters) {
    btnApplyFilters.addEventListener("click", () => {
      loadBooks();
    });
  }

  async function loadBooks() {
    const title = (document.getElementById("searchTitle")?.value || "").trim();
    const author = (document.getElementById("author")?.value || "").trim();
    const catCheckboxes = document.querySelectorAll('input[name="categories"]:checked');
    const categories = Array.from(catCheckboxes).map(cb => cb.value);
    const yearFrom = (document.getElementById("yearFrom")?.value || "").trim();
    const yearTo = (document.getElementById("yearTo")?.value || "").trim();

    const params = new URLSearchParams();
    if (title) params.append("title", title);
    if (author) params.append("author", author);
    if (categories.length > 0) {
      params.append("categories", categories.join(","));
    }
    if (yearFrom) params.append("year_from", yearFrom);
    if (yearTo) params.append("year_to", yearTo);

    try {
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

  async function toggleFavorite(bookId, isFavorite, heartIcon) {
    const method = isFavorite ? "DELETE" : "POST";
    try {
      const response = await fetch("/api/preferences/book", {
        method: method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ book_id: bookId }),
      });
      if (!response.ok) {
        throw new Error("Failed to update favorite status");
      }
      heartIcon.style.color = isFavorite ? "gray" : "red";
    } catch (err) {
      console.error("Error updating favorite:", err);
    }
  }

  function renderBooks(books) {
    resultsContainer.innerHTML = "";

    if (!books || books.length === 0) {
      noResultsMsg.style.display = "block";
      return;
    }
    noResultsMsg.style.display = "none";

    books.forEach(book => {
      const card = document.createElement("div");
      card.classList.add("grid-item", "book-card");
      card.style.position = "relative";

      const coverWrapper = document.createElement("div");
      coverWrapper.classList.add("cover-wrapper");
      const img = document.createElement("img");
      img.alt = `${book.title} cover`;
      img.src = book.cover ? `${book.cover}` : `/static/img/bookCover.png`;
      coverWrapper.appendChild(img);
      coverWrapper.addEventListener("click", () => {
        window.open(`/book/${book.id}`, "_blank");
      });

      card.appendChild(coverWrapper);

      const infoDiv = document.createElement("div");
      infoDiv.classList.add("book-info");

      const titleEl = document.createElement("h3");
      titleEl.classList.add("book-title");
      titleEl.textContent = book.title;
      infoDiv.appendChild(titleEl);

      const authorEl = document.createElement("p");
      authorEl.classList.add("book-author");
      authorEl.textContent = `By: ${book.author}`;
      infoDiv.appendChild(authorEl);

      if (book.categories && book.categories.length > 0) {
        const catEl = document.createElement("p");
        catEl.classList.add("book-categories");
        catEl.innerHTML = `<strong>Categories:</strong> ${book.categories.join(", ")}`;
        infoDiv.appendChild(catEl);
      }

      if (book.publishDate) {
        const yearEl = document.createElement("p");
        yearEl.classList.add("book-year");
        yearEl.innerHTML = `<strong>Published:</strong> ${book.publishDate}`;
        infoDiv.appendChild(yearEl);
      }

      const heartIcon = document.createElement("i");
      heartIcon.classList.add("fa", "fa-heart");
      heartIcon.style.cursor = "pointer";
      heartIcon.style.position = "absolute";
      heartIcon.style.right = "10px";
      heartIcon.style.bottom = "10px";
      heartIcon.style.color = book.liked ? "red" : "gray";
      heartIcon.addEventListener("click", () => {
        toggleFavorite(book.id, heartIcon.style.color === "red", heartIcon);
      });

      card.appendChild(infoDiv);
      card.appendChild(heartIcon);
      resultsContainer.appendChild(card);
    });
  }
});
