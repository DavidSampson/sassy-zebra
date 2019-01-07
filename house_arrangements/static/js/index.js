const containers = [
  ...document.querySelectorAll('.container')
];

function getId(string) {
  return string.split('-')[1];
}

var drake = dragula(containers);

drake.on('drop', (el, target, source)=>{
  let body = new FormData();
  body.append('person', getId(el.id));
  body.append('spot', target.parentElement.getAttribute('class'));
  body.append('house', getId(target.closest('.house').id));
  fetch('/', {
    method: 'POST',
    headers:{ 'X-CSRFToken': Cookies.get('csrftoken') },
    body: body
  });
});
