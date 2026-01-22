<script>
  const buttons = document.querySelectorAll(".menu-btn");
  const contents = document.querySelectorAll(".menu-content");

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      buttons.forEach(b => b.classList.remove("active"));
      contents.forEach(c => c.classList.add("hidden"));

      btn.classList.add("active");
      document.getElementById(btn.dataset.target).classList.remove("hidden");
    });
  });
</script>
