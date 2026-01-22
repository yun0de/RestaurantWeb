<script>
document.addEventListener("DOMContentLoaded", () => {

  const hero = document.getElementById("hero");
  const images = document.querySelectorAll(".hero-image");
  const texts = document.querySelectorAll(".hero-text-slide");

  let current = 0;
  let interval = null;
  const DELAY = 4000;

  function showSlide(index) {
    images.forEach((img, i) => {
      img.classList.toggle("is-active", i === index);
    });

    texts.forEach((txt, i) => {
      txt.classList.toggle("is-active", i === index);
    });
  }

  function startSlider() {
    if (interval) return; // zabrání vícenásobnému intervalu
    interval = setInterval(() => {
      current = (current + 1) % images.length;
      showSlide(current);
    }, DELAY);
  }

  function stopSlider() {
    clearInterval(interval);
    interval = null;
  }

  // INIT
  showSlide(current);
  startSlider();

  // 🟢 PAUSE ON HOVER
  hero.addEventListener("mouseenter", stopSlider);
  hero.addEventListener("mouseleave", startSlider);
  hero.addEventListener("focusin", stopSlider);
  hero.addEventListener("focusout", startSlider);

});
</script>
