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

// db.memberships.ensureIndex({organization_id: 1, role: 1})
print('\nOrganizations without any unique roles:');
db.organizations.find().forEach(function (organization) {
  if (!/\/legislature$/.test(organization.jurisdiction_id)) {
    expect(db.memberships.count({organization_id: organization._id, role: {$in: uniqueRoles}}), [1, 2],
      [organization.jurisdiction_id, organization._id].join(' '));
  }
});

print('\nOrganizations without any non-unique roles:');
db.organizations.find().forEach(function (organization) {
  if (!/\/legislature$/.test(organization.jurisdiction_id)) {
    expect(db.memberships.count({organization_id: organization._id, role: {$in: roles}}), [1, 338],
      [organization.jurisdiction_id, organization._id].join(' '));
  }
});

print('\nOrganizations with multiple unique roles:');
db.organizations.find().forEach(function (organization) {
  uniqueRoles.forEach(function (role) {
    expect(db.memberships.count({organization_id: organization._id, role: role}), [0, 1],
      [organization.jurisdiction_id, organization._id, role].join(' '));
  });
});
