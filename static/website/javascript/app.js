$('.main-carousel').flickity({
    // options
    cellAlign: 'left',
    autoPlay: 3500,
    freeScroll: true,
    contain: true,
    groupCells: true,
    pageDots: true,
    draggable: true,
    lazyLoad: true,
    wrapAround: true,
    prevNextButtons: true,
  });
  
  $('.carousel').flickity({
    // options
    cellAlign: 'left',
    contain: true,
    draggable: true,
    groupCells: true,
    pageDots: false,
     wrapAround: true,
  });
  
  $('.carousel-brands').flickity({
    // options
    cellAlign: 'left',
    contain: true,
    prevNextButtons: true,
    groupCells: true,
    pageDots: false,
    draggable: true,
     wrapAround: true,
  });
  
  $('.nabs-tabs-carousel').flickity({
    // options
    cellAlign: 'left',
    contain: true,
    prevNextButtons: false,
    groupCells: true,
    pageDots: true,
    draggable: true,
     wrapAround: true,
  });
  
  $('.stores').flickity({
    // options
    draggable: true,
    cellAlign: 'left',
     wrapAround: true,
  });
  
  const view = document.querySelector('#view');
  const hide = document.querySelector('#hide');
  
  
  view.addEventListener('click', () => {
    view.classList.toggle('d-none');
    hide.classList.toggle('d-none');
  })
  
  hide.addEventListener('click', () => {
    view.classList.toggle('d-none');
    hide.classList.toggle('d-none');
  })
  
  const body = document.querySelector('body');
  const openBtn = document.querySelector('.open-sidebar');
  const closeBtn = document.querySelector('.close-sidebar');
  
  openBtn.addEventListener('click', () => {
    body.classList.add('show-sidebar');
  });
  
  closeBtn.addEventListener('click', () => {
    body.classList.remove('show-sidebar');
  });
  
  function sortResults(res) {
    console.log(res);
  }
  
  const sortBtn = document.querySelector('.hid-div-btn');
  const sortDiv = document.querySelector('.hid-div-sm');
  sortBtn.addEventListener('click', () => {
    sortDiv.classList.toggle('d-block');
  });
  
  
  