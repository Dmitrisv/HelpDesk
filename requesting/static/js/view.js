window.addEventListener('DOMContentLoaded', ()=> {
  let thumbnail_image = document.querySelectorAll("#image")
    thumbnail_image.forEach(e => {
      e.addEventListener('click', function () {
        var image = new Image();

        image.src = '../media/'+ e.getAttribute("name");

        var viewer = new Viewer(image, {
          hidden: function () {
            viewer.destroy();
          },
          title: false,
          navbar: false,
          toolbar: false,
          button: false,
        });

        viewer.show();
      });
    });
    });