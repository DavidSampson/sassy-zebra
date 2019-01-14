async function printData() {
  let houses = d3.select('#work-holder')
    .selectAll('div')
    .data(await getData())
    .enter().append('div')
    .attr('class',d=> d.fields ? 'house' : 'house no-house');

  houses.append(houseText);

  let spots = houses
    .selectAll(':scope > div:not(.house-name)')
    .data(d=>d.spots)
    .enter().append('div')
    .attr('class','spot');

  spots.selectAll(function(d) {
    _.times(d.fields.quantity,() => this.appendChild(newEl('div')));
    return this.childNodes;
  });

  let people = spots.selectAll('div')
    .data(d=>d.people);

  people.enter().append('div')
    .merge(people)
    .attr('class','person')
    .text(d=>d.fields.name);

  var packery = new Packery( '#work-holder', {
    itemSelector: '.house',
    gutter: 10,
    stamp: '.no-house'
  });

  var drake = dragula(
    [...document.querySelectorAll('.spot')],
    { accepts: isOpenContainer }
  );

  drake.on('drop', updateSpot);
}

printData();
