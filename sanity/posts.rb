require 'csv'
require 'open-uri'

File.open('posts.js', 'w') do |f|
  f.write "var posts = {}\n"

  { 'ocd-division/country:ca/province:bc' => 'province-bc-electoral_districts',
    'ocd-division/country:ca/province:sk' => 'province-sk-electoral_districts',
  }.each do |identifier,filename|
    f.write %(posts['#{identifier}'] = []\n)
    CSV.parse(open("https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/#{filename}.csv")) do |row|
      f.write %(posts['#{identifier}'].push("#{row[1]}")\n)
    end
  end

  [ 'ca_census_subdivisions',
  ].each do |filename|
    CSV.parse(open("https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/#{filename}.csv")) do |row|
      f.write %(posts['#{row[0]}'] = ["#{row[1]}"]\n)
    end
  end

  [ 'ca_municipal_subdivisions',
  ].each do |filename|
    CSV.parse(open("https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/#{filename}.csv")) do |row|
      identifier, _, pair = row[0].rpartition('/')
      f.write %(posts['#{identifier}'].push("#{row[1]}")\n)
      if pair[/:\d+\z/]
        alternative_name = pair.capitalize.sub(':', ' ')
        f.write %(posts['#{identifier}'].push("#{alternative_name}")\n) unless row[1] == alternative_name
      end
    end
  end
end
