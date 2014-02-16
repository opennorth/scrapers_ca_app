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

pad = '                                                                                                         ';

print('\nJurisdictions without exactly one organization:');
db.organizations.distinct('jurisdiction_id').forEach(function (jurisdiction_id) {
  if (!/\/municipalities$/.test(jurisdiction_id)) {
    expect(db.organizations.count({jurisdiction_id: jurisdiction_id}), 1, jurisdiction_id);
  }
});

db.memberships.ensureIndex({person_id: 1})
print('\nPeople without exactly one membership:');
db.people.find().forEach(function (person) {
  expect(db.memberships.count({person_id: person._id}), 1, person._id + ' memberships: ' + person.sources[0].url);
});
