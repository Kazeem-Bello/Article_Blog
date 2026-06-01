async function loadBlogDetail() {
  const params = new URLSearchParams(window.location.search);
  const blogId = params.get("id");
  const container = document.getElementById("blog-detail");
  const title = document.getElementById("blog-title");

  if (!blogId) {
    container.innerHTML = `
          <div class="alert alert-danger">No blog ID provided.</div>
        `;
    return;
  }

  try {
    const response = await fetch(`/api/v1/blog/${blogId}`);

    const blog = await response.json();

    if (!response.ok) {
      throw new Error(blog.detail);
    }

    const publishedDate = blog.created_at
      ? new Date(blog.created_at).toLocaleDateString()
      : "No date";

    title.innerHTML = `${blog.title}`;

    container.innerHTML = `
          <div class="card">
            <div class="card-header">
              <h3>${blog.title}</h3>
            </div>

            <div class="card-body">
              <p class="text-muted">Date Published: ${publishedDate}</p>

              <p class="card-text">
                ${blog.content || "No content available"}
              </p>

              <a href="/" class="btn btn-outline-success">Back to blogs</a>
            </div>
          </div>
        `;
  } catch (error) {
    document.getElementById("blog-detail").innerHTML = `
          <div class="alert alert-danger">
            Could not load this blog.
          </div>
        `;
  }
}

loadBlogDetail();
