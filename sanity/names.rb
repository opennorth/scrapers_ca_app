require 'csv'
require 'open-uri'

File.open('names.js', 'w') do |f|
  f.write "var names = {}\n"

  %w(ca_provinces_and_territories ca_census_divisions ca_census_subdivisions).each do |filename|
    CSV.parse(open("https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/#{filename}.csv")) do |row|
      f.write %(names['#{row[0]}'] = "#{row[1]}"\n)
    end
  end
end
