window.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('.chat-container');

  container.addEventListener('click', (event) => {
    if (event.target.matches('#image')) {
      const e = event.target;
      const image = new Image();
      image.src = e.getAttribute('name');

      const viewer = new Viewer(image, {
        hidden: () => {
          viewer.destroy();
        },
        title: false,
        navbar: false,
        toolbar: false,
        button: false,
      });

      viewer.show();
    }
  });
});