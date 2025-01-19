document.addEventListener("DOMContentLoaded", () => {
  const myListContainer = document.getElementById("myListContainer");
  const noResultsMsg = document.getElementById("noResultsMsg");

  loadMyList();

  async function loadMyList() {
    try {
      const response = await fetch("/api/preferences/data/books");
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      const data = await response.json();
      renderMyList(data);
    } catch (err) {
      console.error("Error fetching book list:", err);
      myListContainer.innerHTML = `<p style="color:red;">Error loading data.</p>`;
    }
  }

  async function removeBook(bookId, cardElement) {
    try {
      const response = await fetch("/api/preferences/book", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ book_id: bookId }),
      });
      if (!response.ok) {
        throw new Error("Failed to remove book from list");
      }
      cardElement.remove();
      if (myListContainer.children.length === 0) {
        noResultsMsg.style.display = "block";
      }
    } catch (err) {
      console.error("Error removing book:", err);
    }
  }

  function renderMyList(books) {
    myListContainer.innerHTML = "";

    if (!books || books.length === 0) {
      noResultsMsg.style.display = "block";
      myListContainer.style.display = "none";
      return;
    }
    noResultsMsg.style.display = "none";

    books.forEach(book => {
      const card = document.createElement("div");
      card.classList.add("grid-item", "book-card");

      const coverWrapper = document.createElement("div");
      coverWrapper.classList.add("cover-wrapper");
      const img = document.createElement("img");
      img.alt = `${book.title} cover`;
      img.src = book.cover ? `${book.cover}` : "/static/img/bookCover.png";
      coverWrapper.appendChild(img);
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

      const removeBtn = document.createElement("button");
      removeBtn.textContent = "Remove";
      removeBtn.classList.add("btn-remove");
      removeBtn.addEventListener("click", () => removeBook(book.id, card));
      card.appendChild(removeBtn);

      card.appendChild(infoDiv);
      myListContainer.appendChild(card);
    });
  }
});
