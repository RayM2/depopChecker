(function () {
  let currentUrl = window.location.href;

  function isProductPage(url) {
    return url.startsWith("https://www.depop.com/products/");
  }

  function injectShoelaceAndFont() {
    // Shoelace JS
    if (!document.getElementById("shoelace-cdn")) {
      const script = document.createElement("script");
      script.type = "module";
      script.src = "https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.11.1/dist/shoelace.js";
      script.id = "shoelace-cdn";
      document.head.appendChild(script);
    }

    // Shoelace CSS Theme
    if (!document.getElementById("shoelace-css")) {
      const css = document.createElement("link");
      css.rel = "stylesheet";
      css.href = "https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.11.1/dist/themes/light.css";
      css.id = "shoelace-css";
      document.head.appendChild(css);
    }

    // Grandstander Font
    if (!document.getElementById("grandstander-font")) {
      const font = document.createElement("link");
      font.rel = "stylesheet";
      font.href = "https://fonts.googleapis.com/css2?family=Grandstander&display=swap";
      font.id = "grandstander-font";
      document.head.appendChild(font);
    }
  }

  function insertPanel() {
    if (document.getElementById("price-checker-panel")) return;

    injectShoelaceAndFont();

    const panel = document.createElement("div");
    panel.id = "price-checker-panel";
    panel.style.position = "fixed";
    panel.style.top = "80px";
    panel.style.right = "20px";
    panel.style.width = "320px";
    panel.style.zIndex = "9999";
    panel.style.fontFamily = "'Grandstander', sans-serif";
    panel.style.backgroundColor = "#e6f0ff"; // retro pop background
    panel.style.color = "#222222";
    panel.style.border = "1px solid #ccc";
    panel.style.borderRadius = "10px";
    panel.style.boxShadow = "0 4px 12px rgba(0,0,0,0.1)";
    panel.style.padding = "10px";

    panel.innerHTML = `
      <sl-card>
        <div style="font-family: 'Grandstander', sans-serif; font-size: 14px; color: #222222;">
          <h3 style="margin-top: 0; margin-bottom: 10px;">Retail Price Checker</h3>
          <div id="price-list">
            <sl-spinner style="font-size: 1.5rem;" aria-label="Loading..."></sl-spinner>
          </div>
        </div>
      </sl-card>
    `;

    document.body.appendChild(panel);
  }

  async function updatePanel() {
    const listContainer = document.getElementById("price-list");
    const onProductPage = isProductPage(window.location.href);

    if (!onProductPage) {
      if (listContainer) {
        listContainer.innerHTML = `<p>Select a product to see price comparisons.</p>`;
      }
      return;
    }

    const titleEl = document.querySelector('h1[data-testid="listing-title"]') || document.querySelector("h1");
    const descEl = document.querySelector('p[class*="styles_textWrapper__"]');

    let query = "";
    if (descEl && descEl.innerText.trim().length > 20) {
      query = descEl.innerText.trim();
    } else if (titleEl) {
      query = titleEl.innerText.trim();
    }

    if (!query) {
      listContainer.innerHTML = `<p>Could not find a product title or description.</p>`;
      return;
    }

    listContainer.innerHTML = `<sl-spinner style="font-size: 1.5rem;" aria-label="Loading..."></sl-spinner>`;

    try {
      const res = await fetch(`http://localhost:5000/api/search?q=${encodeURIComponent(query)}`);
      const data = await res.json();

      if (!Array.isArray(data) || data.length === 0) {
        listContainer.innerHTML = `<p>No results found.</p>`;
        return;
      }

      const listHTML = data.map(result => {
        const price = result.price && result.price !== "N/A" ? `<strong> – ${result.price}</strong>` : "";
        return `
          <div style="margin-bottom: 8px;">
            <a href="${result.link}" target="_blank" style="color: #ff6b6b; text-decoration: none;">
              ${result.title}
            </a>${price}
          </div>`;
      }).join("");

      listContainer.innerHTML = listHTML;

    } catch (err) {
      console.error("Error fetching results:", err);
      listContainer.innerHTML = `<p>Error fetching price data.</p>`;
    }
  }

  function checkForUpdates() {
    const newUrl = window.location.href;
    if (newUrl !== currentUrl) {
      currentUrl = newUrl;
      insertPanel();
      updatePanel();
    }
  }

  insertPanel();
  updatePanel();
  setInterval(checkForUpdates, 1000);
})();
