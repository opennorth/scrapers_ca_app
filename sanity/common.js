var pad = '                                        ';

var roles = [
  // Provincial
  'MHA',
  'MLA',
  'MNA',
  'MPP',
  // Municipal
  'Alderman',
  'Area Councillor',
  'Councillor',
  'Local Councillor',
  'Regional Councillor',
];

var uniqueRoles = [
  // Provincial
  'Premier',
  // Municipal
  'Acting Chief Administrative Officer',
  'Chairperson',
  'Chief Administrative Officer',
  'Chief Executive Officer',
  'City Manager',
  'Mayor', 'Deputy Mayor',
  'Municipal Administrator',
  'Reeve', 'Deputy Reeve',
  'Warden', 'Deputy Warden',
];

var expect = function (actual, expected, message) {
  if (toString.call(expected) === '[object Array]') {
    var minimum = expected[0]
      , maximum = expected[1];
    if (actual < minimum || maximum < actual) {
      print(message + ': ' + actual + ' (expected in [' + expected + '])');
    }
  }
  else if (expected !== actual) {
    print(message + ': ' + actual + ' (expected == ' + expected + ')');
  }
};

var mapReduce = function (collection, map) {
  db[collection].mapReduce(map, function (key, values) {
    return Array.sum(values);
  }, {out: {inline: 1}}).results.forEach(function (result) {
    print(result._id + pad.substring(0, 40 - result._id.length) + result.value);
  });
}

var division_id_from_jurisdiction_id = function (jurisdiction_id) {
  return jurisdiction_id.replace('jurisdiction', 'division').replace(/\/(?:council|legislature)$/, '');
};
