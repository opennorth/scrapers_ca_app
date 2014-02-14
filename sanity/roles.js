// @todo Move into models?
print('\nOrganizations with unexpected roles:');
db.organizations.find().forEach(function (organization) {
  // @todo In "municipalities" scrapers, need to tag each organization with its
  // OCD ID, in order to validate its styles of address.
  if (!/\/municipalities$/.test(organization.jurisdiction_id)) {
    var division_id = division_id_from_jurisdiction_id(organization.jurisdiction_id);
    if (styles[division_id]) {
      var difference = db.memberships.distinct('role', {organization_id: organization._id}).filter(function (x) {
        return styles[division_id].indexOf(x) === -1;
      });
      expect(difference.length, 0, [organization.jurisdiction_id, organization._id].concat(difference).join(' '));
    }
    else {
      print('No styles of address for ' + division_id);
    }
  }
});

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
