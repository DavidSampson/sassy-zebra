const containers = [
  ...document.querySelectorAll('div.house-container'),
  document.querySelector('div.people')
];

var drake = dragula(containers);
