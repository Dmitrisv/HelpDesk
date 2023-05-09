window.addEventListener('DOMContentLoaded', ()=> {
  let thumbnail_image = document.querySelector("img")
      image.addEventListener('click', function () {
        var image = new Image();

        image.src = '../media/'+ thumbnail_image.getAttribute("name");

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