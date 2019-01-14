// function makeBody(obj) {
//   let body = new FormData();
//   Object.entries(obj).forEach(i => body.append(...i));
//   return body;
// }

// function updateSpot(el, target, source){
//   fetch('/', {
//     method: 'POST',
//     headers:{ 'X-CSRFToken': Cookies.get('csrftoken') },
//     body:
//   });
// }

function RemoveAppFromModel(obj) {
  return  _.update(obj, 'model', k=> _.last(k.split('.')))
}

function FlattenModel(arr) {
  return ({[arr[0].model]: arr.map(j => _.omit(j, ['model']))});
}

function APIUrl(path){
  return `/api/${path}`
}

async function getData() {
  return _.chain(
    await Promise.all(
      _(['people','spots','houses'])
        .map(APIUrl)
        .map(_.unary(d3.json))))
    .map(JSON.parse)
    .map(i => i.map(RemoveAppFromModel))
    .map(FlattenModel)
    .reduce((i,j) => Object.assign(j,i), {})
    .tap(d => {
      d.house.push({pk: null});
      d.spot.push({pk: null, fields: {house: null, quantity: 1}});

      d.house.forEach(i => _.assign(i, {spots: []}));
      d.spot.forEach(i => _.assign(i, {people: []}));

      d.person.forEach(i => _.find(d.spot, j => j.pk === i.fields.spot).people.push(i));
      d.spot.forEach(i => _.find(d.house, j => j.pk === i.fields.house).spots.push(i));
      console.log(d.house);
      return d;
    })
    .get('house')
    .value();
}

const newEl = sel => document.createElement(sel);

function removePerson(person, spot) {
  _.remove(spot.people, i => i.pk === person.pk);
  return spot;
}

function addPerson(person, spot) {
  spot.people.push(person);
  return spot;
}

function setSpot(person, spot) {
  person.fields.spot = spot.pk;
  return person;
}

function updateSpot(el, target, source) {
  let person = d3.select(el);
  let from = d3.select(source);
  let to = d3.select(target);
  if(from.datum().pk !== to.datum().pk ) {
    from.datum(d => removePerson(person.datum(), d));
    to.datum(d => addPerson(person.datum(), d));

    person.datum(d => setSpot(d, to.datum()));

    if(from.datum().pk !== 0) from.append('div');
    to.select('div:not(.person)').remove();
  }
}

function isOpenContainer(_, target) {
  let dest = d3.select(target).datum();
  return dest.people.length < dest.fields.quantity || !dest.fields.house;
}

const createIcon = i => {
  let icon = document.createElement('i');
  icon.className = i;
  return icon;
};

const catIconS = "fas fa-cat";
const dogIconS = "fas fa-dog";
const earlyIconS = 'fab fa-earlybirds';
const noiseIconS = 'fas fa-volume-up';



function houseText(d) {
  let container = document.createElement('div');
  container.className = 'house-name';
  let name = document.createElement('span');
  name.innerHTML = d.fields ? d.fields.name : 'No house';
  container.appendChild(name);
  let iconContainer = document.createElement('div');
  iconContainer.className = 'house-icons';
  container.appendChild(iconContainer);
  if(d.fields) {
    // /*if(d.fields.cats)*/ iconContainer.appendChild(createIcon(catIconS));
    let cat = createIcon(catIconS);
    cat.className += ' disabled-icon';
    iconContainer.appendChild(cat);
    /*if(d.fields.dogs)*/ iconContainer.appendChild(createIcon(dogIconS));
    /*if(d.fields.early_up)*/ iconContainer.appendChild(createIcon(earlyIconS));
    /*if(d.fields.noise)*/ iconContainer.appendChild(createIcon(noiseIconS));
  }
  return container;
}
