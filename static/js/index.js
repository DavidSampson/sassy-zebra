const containers = [
  ...document.querySelectorAll('.container')
];

function getId(string) {
  return Number(string.split('-')[1]);
}

var drake = dragula(containers, {
  accepts: (_, target) => target.id == 'people-container' || target.childElementCount == 0
});

drake.on('drop', (el, target, source)=>{
  let body = new FormData();
  body.append('person', getId(el.id));
  let spot = target.id == 'people-container' ? -1 : getId(target.closest('.spot').id);
  body.append('spot', spot);
  fetch('/', {
    method: 'POST',
    headers:{ 'X-CSRFToken': Cookies.get('csrftoken') },
    body: body
  });
});
