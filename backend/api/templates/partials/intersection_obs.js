<script>
document.addEventListener("DOMContentLoaded", () => {

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          obs.unobserve(entry.target); // animate once
        }
      });
    },
    {
      threshold: 0.15
    }
  );

  // Observe ALL fade-in variants
  document.querySelectorAll(
    ".fade-in, .fade-in2"
  ).forEach(el => {
    observer.observe(el);
  });

});
</script>
