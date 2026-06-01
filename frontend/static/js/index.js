async function loadBlogs() {
  try {
    const response = await fetch("/api/v1/blog/");
    const blogs = await response.json();

    if (!response.ok) {
      throw new Error(blogs.detail);
    }

    const container = document.getElementById("blogs-container");
    container.innerHTML = "";

    blogs.forEach((blog) => {
      const publishedDate = blog.created_at
        ? new Date(blog.created_at).toLocaleDateString()
        : "No date";

      const shortContent = blog.content
        ? blog.content.substring(0, 60) + "..."
        : "No content available";

      const blogCard = `
          <div class="col-sm-4 mb-4">
            <div class="card h-100">
              <div class="card-header">
                ${blog.title}
              </div>

              <div class="card-body">
                <p class="card-text">
                  Date Published: ${publishedDate}
                </p>

                <small class="card-text text-muted">
                  Content: ${shortContent}
                </small>

                <br><br>

                <a href="/blog.html?id=${blog.id}" class="btn btn-outline-success">
                  Read more
                </a>
              </div>
            </div>
          </div>
        `;

      container.innerHTML += blogCard;
    });
  } catch (error) {
    console.error(error);

    const container = document.getElementById("blogs-container");
    container.innerHTML = `
        <div class="col-12">
          <div class="alert alert-danger">
            Could not load blogs. Please try again.
          </div>
        </div>
      `;
  }
}

loadBlogs();
