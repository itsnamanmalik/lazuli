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
  
  
  

// USER PROFILE
var wallet = document.getElementById('wallet');
var addresses = document.getElementById('addresses');
var editProfile = document.getElementById('edit-profile');
var item1 = document.getElementById('item-1');
var item2 = document.getElementById('item-2');
var item3 = document.getElementById('item-3');

item1.addEventListener('click', () => {
  wallet.classList.remove('d-none');
  addresses.classList.add('d-none');
  editProfile.classList.add('d-none');
  item1.classList.add('border-bottom-gray');
  item2.classList.remove('border-bottom-gray');
  item3.classList.remove('border-bottom-gray');
});

item2.addEventListener('click', () => {
  wallet.classList.add('d-none');
  addresses.classList.remove('d-none');
  editProfile.classList.add('d-none');
  item2.classList.add('border-bottom-gray');
  item1.classList.remove('border-bottom-gray');
  item3.classList.remove('border-bottom-gray');
});

item3.addEventListener('click', () => {
  wallet.classList.add('d-none');
  addresses.classList.add('d-none');
  editProfile.classList.remove('d-none');
  item3.classList.add('border-bottom-gray');
  item1.classList.remove('border-bottom-gray');
  item2.classList.remove('border-bottom-gray');
});


