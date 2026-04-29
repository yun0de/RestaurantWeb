<script>
  const buttons = document.querySelectorAll(".menu-btn");
  const contents = document.querySelectorAll(".menu-content");

  function activateMenu(targetId, updateHash = true) {
    const targetButton = document.querySelector(`.menu-btn[data-target="${targetId}"]`);
    const targetContent = document.getElementById(targetId);

    if (!targetButton || !targetContent) return;

    buttons.forEach(b => b.classList.remove("active"));
    contents.forEach(c => c.classList.add("hidden"));

    targetButton.classList.add("active");
    targetContent.classList.remove("hidden");

    if (updateHash && window.location.hash !== `#${targetId}`) {
      history.replaceState(null, "", `#${targetId}`);
    }
  }

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      activateMenu(btn.dataset.target);
    });
  });

  if (window.location.hash === "#menu-pdf") {
    activateMenu("menu-pdf", false);
  } else {
    activateMenu("menu-html", false);
  }
</script>
