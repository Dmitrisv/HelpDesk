const input = document.querySelector('input[type="file"]');
document.addEventListener('paste', event => {
  const clipboardData = event.clipboardData;

  if (clipboardData.items && clipboardData.items.length) {
    const imageItem = Array.from(clipboardData.items).find(item => item.type.indexOf('image') !== -1);

    if (imageItem) {
      const imageBlob = imageItem.getAsFile();
      const file = new File([imageBlob], 'image-'+Math.floor(Date.now() / 1000)+".png");

      const filelist = new DataTransfer();
      filelist.items.add(file);

      input.files = filelist.files;
    }
    console.log(input.files);
  }
});