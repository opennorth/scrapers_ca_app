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
    if (expected.indexOf(actual) === -1) {
      print(message + ': ' + actual + ' (expected in [' + expected + '])');
    }
  }
  else if (expected !== actual) {
    print(message + ': ' + actual + ' (expected == ' + expected + ')');
  }
};

var expectNone = function (collection, field) {
  var selector = {};
  selector[field] = {$exists: true};
  expect(db[collection].count(selector), 0, collection + ' ' + field + ' count');
};

var mapReduce = function (collection, map) {
  db[collection].mapReduce(map, function (key, values) {
    return Array.sum(values);
  }, {out: {inline: 1}}).results.forEach(function (result) {
    print(result._id + pad.substring(0, 40 - result._id.length) + result.value);
  });
}

// Finds documents in the given collection matching the given criteria. If any
// documents are found, prints the given message and, for each document, prints
// its ID and the value of the given field.
var matches = function (collection, field, criteria, message) {
  message = message || collection + ' with invalid ' + field;

  var count = db[collection].count(criteria);
  if (count) {
    print('\n' + message + ':');
    db[collection].find(criteria).forEach(function (obj) {
      if (field.indexOf('.') === -1) {
        print(obj._id + ': ' + obj[field]);
      }
      else {
        print(obj._id);
      }
    });
  }
};

var division_id_from_jurisdiction_id = function (jurisdiction_id) {
  return jurisdiction_id.replace('jurisdiction', 'division').replace(/\/(?:council|legislature)$/, '');
};
