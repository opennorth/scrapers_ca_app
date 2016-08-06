# DO NOT EDIT THIS AUTO-GENERATED FILE
import re

from django.template.defaultfilters import slugify

leading_zero_re = re.compile(r'^0+')
invalid_re = re.compile(r'[^a-z\d._~-]')
leading_district_re = re.compile(r'^District ')
lower = lambda boundary: boundary['external_id'].lower()

matcher = lambda boundary: leading_district_re.sub('', leading_zero_re.sub('', invalid_re.sub('~', boundary['name'].lower().replace(' ', '_'))))

suffix = lambda suffix: lambda boundary: boundary['external_id'] + suffix

IMAGO_BOUNDARY_MAPPINGS = {
    'acton-vale-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2448028/district:',
    },
    'adstock-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2431056/district:',
    },
    'ahuntsic-cartierville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'ajax-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3518005/ward:',
    },
    'albanel-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2492030/district:',
    },
    'alberta-electoral-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/province:ab/ed:',
    },
    'alma-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2493042/district:',
    },
    'amherst-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2478070/district:',
    },
    'amqui-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2407047/district:',
    },
    'ange-gardien-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2455008/district:',
    },
    'anjou-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'baie-comeau-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2496020/district:',
    },
    'baie-saint-paul-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2416013/district:',
    },
    'barraute-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2488022/district:',
    },
    'bas-caraquet-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1315027/ward:',
    },
    'beaconsfield-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466107/district:',
    },
    'beaubassin-east-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1307005/ward:',
    },
    'beauceville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2427028/district:',
    },
    'beauharnois-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2470022/district:',
    },
    'beaumont-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2419105/district:',
    },
    'beauport-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2423027/district:',
    },
    'belledune-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1314025/ward:',
    },
    'belleville-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3512005/ward:',
    },
    'beloeil-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2457040/district:',
    },
    'beresford-wards': {
        'boundary_key': matcher,
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1315015/ward:',
    },
    'berthierville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2452035/district:',
    },
    'birch-hills-no-460-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4715067/division:',
    },
    'blainville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2473015/district:',
    },
    'boisbriand-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2473005/district:',
    },
    'boischatel-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2421045/district:',
    },
    'bone-creek-no-108-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4704058/division:',
    },
    'bonnyville-no-87-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4812004/ward:',
    },
    'boucherville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2458033/district:',
    },
    'brampton-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3521010/ward:',
    },
    'brantford-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3529006/ward:',
    },
    'british-columbia-electoral-districts': {
        'boundary_key': lower,
        'key': 'id',
        'prefix': 'ocd-division/country:ca/province:bc/ed:',
    },
    'british-columbia-electoral-districts-2015-redistribution': {
        'boundary_key': lower,
        'key': 'id',
        'prefix': 'ocd-division/country:ca/province:bc/ed:',
    },
    'bromont-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2446078/district:',
    },
    'brompton-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2443027/district:',
    },
    'brossard-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2458007/district:',
    },
    'brownsburg-chatham-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2476043/district:',
    },
    'buffalo-no-409-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4713068/division:',
    },
    'burlington-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3524002/ward:',
    },
    'caledon-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3521024/ward:',
    },
    'caledonia-no-99-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4702066/division:',
    },
    'calgary-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4806016/ward:',
    },
    'cambridge-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3530010/ward:',
    },
    'campobello-island-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1302004/ward:',
    },
    'canaan-no-225-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4707058/division:',
    },
    'candiac-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2467020/district:',
    },
    'cantley-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2482020/district:',
    },
    'cap-chat-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2404047/district:',
    },
    'cap-sante-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2434030/district:',
    },
    'cape-breton-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1217030/district:',
    },
    'caraquet-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1315028/ward:',
    },
    'carignan-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2457010/district:',
    },
    'causapscal-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2407018/district:',
    },
    'chambly-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2457005/district:',
    },
    'chandler-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2402028/district:',
    },
    'charlemagne-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2460005/district:',
    },
    'charlesbourg-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2423027/district:',
    },
    'charlottetown-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1102075/ward:',
    },
    'chateauguay-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2467050/district:',
    },
    'chatham-kent-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3536020/ward:',
    },
    'chelsea-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2482025/district:',
    },
    'chertsey-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2462047/district:',
    },
    'chicoutimi-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2494068/district:',
    },
    'clarington-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3518017/ward:',
    },
    'clayton-no-333-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4709067/division:',
    },
    'clermont-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2415035/district:',
    },
    'cleveland-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2442110/district:',
    },
    'cloridorme-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2403010/district:',
    },
    'compton-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2444071/district:',
    },
    'connaught-no-457-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4714056/division:',
    },
    'contrecoeur-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2459035/district:',
    },
    'cookshire-eaton-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2441038/district:',
    },
    'cote-des-neigesnotre-dame-de-grace-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'cote-saint-luc-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466058/district:',
    },
    'coteau-du-lac-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2471040/district:',
    },
    'cowansville-quartiers': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2446080/quartier:',
    },
    'delson-quartiers': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2467025/quartier:',
    },
    'desbiens-quartiers': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2493005/quartier:',
    },
    'deux-montagnes-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2472010/district:',
    },
    'dieppe-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1307045/ward:',
    },
    'dollard-des-ormeaux-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466142/district:',
    },
    'dorval-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466087/district:',
    },
    'drummondville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2449058/district:',
    },
    'dunham-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2446050/district:',
    },
    'east-broughton-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2431122/district:',
    },
    'east-hants-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1208008/district:',
    },
    'edenwold-no-158-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4706029/division:',
    },
    'edmonton-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4811061/ward:',
    },
    'edmundston-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1313027/ward:',
    },
    'elcapo-no-154-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4705028/division:',
    },
    'elfros-no-307-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4710041/division:',
    },
    'estevan-no-5-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4701022/division:',
    },
    'excelsior-no-166-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4707021/division:',
    },
    'farnham-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2446112/district:',
    },
    'federal-electoral-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/ed:',
    },
    'fish-creek-no-402-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4715036/division:',
    },
    'fleurimont-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2443027/district:',
    },
    'florenceville-bristol-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1311027/ward:',
    },
    'fossambault-sur-le-lac-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2422010/district:',
    },
    'fredericton-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1310032/ward:',
    },
    'frenchman-butte-no-501-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4717032/division:',
    },
    'frontenac-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2430025/district:',
    },
    'gaspe-quartiers': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2403005/quartier:',
    },
    'gatineau-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2481017/district:',
    },
    'granby-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2447017/district:',
    },
    'grand-falls-wards': {
        'boundary_key': matcher,
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1312019/ward:',
    },
    'grande-prairie-county-no-1-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4819006/division:',
    },
    'grande-riviere-quartiers': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2402015/quartier:',
    },
    'gravelbourg-no-104-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4703068/division:',
    },
    'greater-sudbury-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3553005/ward:',
    },
    'greenfield-park-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2458227/district:',
    },
    'grimsby-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3526065/ward:',
    },
    'guelph-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3523008/ward:',
    },
    'gull-lake-no-139-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4708009/division:',
    },
    'haldimand-county-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3528018/ward:',
    },
    'halifax-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1209034/district:',
    },
    'hamilton-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3525005/ward:',
    },
    'happy-valley-no-10-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4702018/division:',
    },
    'hart-butte-no-11-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4703001/division:',
    },
    'hebertville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2493020/district:',
    },
    'hudson-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2471100/district:',
    },
    'huntingdon-quartiers': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2469055/quartier:',
    },
    'jacques-cartier-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2443027/district:',
    },
    'joliette-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2461025/district:',
    },
    'jonquiere-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2494068/district:',
    },
    'kawartha-lakes-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3516010/ward:',
    },
    'kedgwick-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1314019/ward:',
    },
    'kingsley-no-124-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4705014/division:',
    },
    'kingston-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3510010/ward:',
    },
    'kirkland-districts': {
        'boundary_key': matcher,
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466102/district:',
    },
    'kitchener-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3530013/ward:',
    },
    'la-baie-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2494068/district:',
    },
    'la-cite-limoilou-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2423027/district:',
    },
    'la-haute-saint-charles-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2423027/district:',
    },
    'la-malbaie-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2415013/district:',
    },
    'la-peche-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2482035/district:',
    },
    'la-prairie-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2467015/district:',
    },
    'la-sarre-quartiers': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2487090/quartier:',
    },
    'la-tuque-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2490012/district:',
    },
    'lac-au-saumon-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2407057/district:',
    },
    'lac-brome-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2446075/district:',
    },
    'lac-des-ecorces-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2479078/district:',
    },
    'lac-des-seize-iles-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2477055/district:',
    },
    'lac-megantic-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2430030/district:',
    },
    'lac-pelletier-no-107-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4704061/division:',
    },
    'lac-saint-joseph-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2422015/district:',
    },
    'lac-sergent-quartiers': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2434120/quartier:',
    },
    'lac-superieur-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2478095/district:',
    },
    'lachine-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'lachute-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2476020/district:',
    },
    'lancienne-lorette-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2423057/district:',
    },
    'lange-gardien-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2482005/district:',
    },
    'lanoraie-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2452017/district:',
    },
    'lasalle-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'lascension-de-notre-seigneur-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2493065/district:',
    },
    'lassomption-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2460028/district:',
    },
    'last-mountain-valley-no-250-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4711003/division:',
    },
    'laval-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2465005/district:',
    },
    'lavaltrie-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2452007/district:',
    },
    'le-vieux-longueuil-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2458227/district:',
    },
    'leduc-county-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4811012/division:',
    },
    'lennoxville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2443027/district:',
    },
    'lepiphanie-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2460035/district:',
    },
    'lery-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2467055/district:',
    },
    'les-cedres-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2471050/district:',
    },
    'les-coteaux-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2471033/district:',
    },
    'les-iles-de-la-madeleine-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2401023/district:',
    },
    'les-rivieres-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2423027/district:',
    },
    'levis-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2425213/district:',
    },
    'lile-bizardsainte-genevieve-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'lile-perrot-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2471060/district:',
    },
    'lincoln-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3526057/ward:',
    },
    'lislet-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2417078/district:',
    },
    'london-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3539036/ward:',
    },
    'longueuil-boroughs': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2458227/borough:',
    },
    'longueuil-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2458227/district:',
    },
    'lunenburg-districts': {
        'boundary_key': lower,
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1206001/district:',
    },
    'lyster-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2432065/district:',
    },
    'macamic-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2487058/district:',
    },
    'magog-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2445072/district:',
    },
    'malartic-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2489015/district:',
    },
    'mandeville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2452095/district:',
    },
    'manitoba-electoral-districts': {
        'boundary_key': matcher,
        'key': 'id',
        'prefix': 'ocd-division/country:ca/province:mb/ed:',
    },
    'maniwaki-quartiers': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2483065/quartier:',
    },
    'marieville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2455048/district:',
    },
    'markham-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3519036/ward:',
    },
    'maryfield-no-91-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4701094/division:',
    },
    'mascouche-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2464015/district:',
    },
    'matane-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2408053/district:',
    },
    'mcmasterville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2457025/district:',
    },
    'memramcook-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1307013/ward:',
    },
    'mercier-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2467045/district:',
    },
    'mercierhochelaga-maisonneuve-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'metabetchouanlac-a-la-croix-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2493012/district:',
    },
    'milton-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3524009/ward:',
    },
    'mirabel-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2474005/district:',
    },
    'mississauga-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3521005/ward:',
    },
    'moncton-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1307022/ward:',
    },
    'mont-bellevue-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2443027/district:',
    },
    'mont-joli-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2409077/district:',
    },
    'mont-royal-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466072/district:',
    },
    'mont-saint-hilaire-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2457035/district:',
    },
    'mont-tremblant-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2478102/district:',
    },
    'montcalm-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2478055/district:',
    },
    'montmagny-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2418050/district:',
    },
    'montmartre-no-126-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4706001/division:',
    },
    'montreal-boroughs': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/borough:',
    },
    'montreal-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'montreal-est-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466007/district:',
    },
    'montreal-nord-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'moose-mountain-no-63-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4701053/division:',
    },
    'nantes-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2430045/district:',
    },
    'new-brunswick-electoral-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/province:nb/ed:',
    },
    'newfoundland-and-labrador-electoral-districts': {
        'boundary_key': matcher,
        'key': 'id',
        'prefix': 'ocd-division/country:ca/province:nl/ed:',
    },
    'newmarket-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3519048/ward:',
    },
    'north-dumfries-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3530004/ward:',
    },
    'northwest-territories-electoral-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/territory:nt/ed:',
    },
    'notre-dame-de-lile-perrot-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2471065/district:',
    },
    'notre-dame-des-bois-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2430010/district:',
    },
    'notre-dame-des-prairies-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2461030/district:',
    },
    'notre-dame-du-mont-carmel-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2437235/district:',
    },
    'nova-scotia-electoral-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/province:ns/ed:',
    },
    'oakville-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3524001/ward:',
    },
    'oka-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2472032/district:',
    },
    'ontario-electoral-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/province:on/ed:',
    },
    'oromocto-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1303012/ward:',
    },
    'ottawa-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3506008/ward:',
    },
    'otterburn-park-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2457030/district:',
    },
    'outremont-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'perce-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2402005/district:',
    },
    'perdue-no-346-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4712050/division:',
    },
    'peterborough-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3515014/ward:',
    },
    'pickering-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3518001/ward:',
    },
    'pierrefonds-roxboro-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'pincourt-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2471070/district:',
    },
    'plateau-mont-royal-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'plessisville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2432040/district:',
    },
    'pohenegamook-quartiers': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2413095/quartier:',
    },
    'pointe-aux-outardes-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2496030/district:',
    },
    'pointe-calumet-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2472020/district:',
    },
    'pointe-claire-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466097/district:',
    },
    'pointe-lebel-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2496025/district:',
    },
    'pontiac-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2482030/district:',
    },
    'port-danielgascons-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2402047/district:',
    },
    'prevost-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2475040/district:',
    },
    'prince-edward-island-electoral-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/province:pe/ed:',
    },
    'princeville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2432033/district:',
    },
    'quebec-boroughs': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2423027/borough:',
    },
    'quebec-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2423027/district:',
    },
    'quebec-electoral-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/province:qc/ed:',
    },
    'ragueneau-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2496040/district:',
    },
    'rawdon-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2462037/district:',
    },
    'regina-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4706027/ward:',
    },
    'repentigny-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2460013/district:',
    },
    'richelieu-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2455057/district:',
    },
    'richmond-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2442098/district:',
    },
    'richmond-hill-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3519038/ward:',
    },
    'rigaud-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2471133/district:',
    },
    'rimouski-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2410043/district:',
    },
    'riverview-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1306020/ward:',
    },
    'riviere-des-prairiespointe-aux-trembles-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'riviere-du-loup-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2412072/district:',
    },
    'rock-rorestsaint-eliedeauville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2443027/district:',
    },
    'rosemontla-petite-patrie-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'rougemont-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2455037/district:',
    },
    'rouyn-noranda-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2486042/district:',
    },
    'roxton-pond-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2447047/district:',
    },
    'rudy-no-284-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4711026/division:',
    },
    'saguenay-boroughs': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2494068/borough:',
    },
    'saguenay-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2494068/district:',
    },
    'saint-agapit-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2433045/district:',
    },
    'saint-alphonse-rodriguez-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2462025/district:',
    },
    'saint-ambroise-de-kildare-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2461040/district:',
    },
    'saint-ambroise-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2494255/district:',
    },
    'saint-andre-dargenteuil-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2476008/district:',
    },
    'saint-andre-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1313002/ward:',
    },
    'saint-anicet-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2469070/district:',
    },
    'saint-antonin-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2412015/district:',
    },
    'saint-aubert-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2417055/district:',
    },
    'saint-augustin-de-desmaures-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2423072/district:',
    },
    'saint-basile-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2434038/district:',
    },
    'saint-basile-le-grand-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2457020/district:',
    },
    'saint-bruno-de-guigues-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2485045/district:',
    },
    'saint-bruno-de-montarville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2458037/district:',
    },
    'saint-bruno-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2493030/district:',
    },
    'saint-calixte-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2463055/district:',
    },
    'saint-cesaire-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2455023/district:',
    },
    'saint-charles-de-bellechasse-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2419097/district:',
    },
    'saint-christophe-darthabaska-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2439060/district:',
    },
    'saint-chrysostome-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2469017/district:',
    },
    'saint-claude-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2442100/district:',
    },
    'saint-colomban-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2475005/district:',
    },
    'saint-comeliniere-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2429057/district:',
    },
    'saint-constant-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2467035/district:',
    },
    'saint-cyrille-de-wendover-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2449070/district:',
    },
    'saint-damase-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2454017/district:',
    },
    'saint-damien-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2462075/district:',
    },
    'saint-david-de-falardeau-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2494245/district:',
    },
    'saint-denis-de-brompton-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2442025/district:',
    },
    'saint-dominique-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2454060/district:',
    },
    'saint-donat-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2462060/district:',
    },
    'saint-esprit-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2463030/district:',
    },
    'saint-eustache-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2472005/district:',
    },
    'saint-fabien-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2410070/district:',
    },
    'saint-faustinlac-carre-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2478047/district:',
    },
    'saint-felix-de-valois-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2462007/district:',
    },
    'saint-ferdinand-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2432013/district:',
    },
    'saint-ferreol-les-neiges-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2421010/district:',
    },
    'saint-flavien-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2433052/district:',
    },
    'saint-francois-xavier-de-brompton-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2442020/district:',
    },
    'saint-fulgence-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2494235/district:',
    },
    'saint-gabriel-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2452080/district:',
    },
    'saint-gedeon-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2493035/district:',
    },
    'saint-georges-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2429073/district:',
    },
    'saint-germain-de-grantham-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2449048/district:',
    },
    'saint-henri-de-taillon-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2493070/district:',
    },
    'saint-henri-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2419068/district:',
    },
    'saint-honore-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2494240/district:',
    },
    'saint-hubert-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2458227/district:',
    },
    'saint-hyacinthe-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2454048/district:',
    },
    'saint-ignace-de-loyola-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2452045/district:',
    },
    'saint-isidore-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2426063/district:',
    },
    'saint-jean-baptiste-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2457033/district:',
    },
    'saint-jean-sur-richelieu-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2456083/district:',
    },
    'saint-jerome-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2475017/district:',
    },
    'saint-john-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1301006/ward:',
    },
    'saint-joseph-de-beauce-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2427043/district:',
    },
    'saint-joseph-de-sorel-quartiers': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2453050/quartier:',
    },
    'saint-joseph-du-lac-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2472025/district:',
    },
    'saint-lambert-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2458012/district:',
    },
    'saint-laurent-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'saint-lazare-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2471105/district:',
    },
    'saint-leonard-daston-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2450042/district:',
    },
    'saint-leonard-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'saint-linlaurentides-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2463048/district:',
    },
    'saint-mathieu-de-beloeil-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2457045/district:',
    },
    'saint-maurice-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2437230/district:',
    },
    'saint-michel-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2468050/district:',
    },
    'saint-nazaire-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2493045/district:',
    },
    'saint-philippe-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2467010/district:',
    },
    'saint-pie-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2454008/district:',
    },
    'saint-placide-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2472043/district:',
    },
    'saint-remi-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2468055/district:',
    },
    'saint-roch-de-lachigan-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2463035/district:',
    },
    'saint-simeon-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2415058/district:',
    },
    'saint-stanislas-de-kostka-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2470040/district:',
    },
    'saint-thomas-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2461027/district:',
    },
    'saint-tite-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2435027/district:',
    },
    'saint-urbain-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2416055/district:',
    },
    'saint-zotique-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2471025/district:',
    },
    'sainte-adele-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2477022/district:',
    },
    'sainte-anne-de-bellevue-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466117/district:',
    },
    'sainte-anne-de-sorel-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2453065/district:',
    },
    'sainte-anne-des-monts-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2404037/district:',
    },
    'sainte-anne-des-plaines-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2473035/district:',
    },
    'sainte-brigitte-de-laval-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2422045/district:',
    },
    'sainte-catherine-de-hatley-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2445060/district:',
    },
    'sainte-catherine-de-la-jacques-cartier-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2422005/district:',
    },
    'sainte-catherine-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2467030/district:',
    },
    'sainte-claire-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2419055/district:',
    },
    'sainte-clotilde-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2468020/district:',
    },
    'sainte-foysillerycap-rouge-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2423027/district:',
    },
    'sainte-genevieve-de-berthier-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2452040/district:',
    },
    'sainte-julie-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2459010/district:',
    },
    'sainte-julienne-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2463060/district:',
    },
    'sainte-marthe-sur-le-lac-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2472015/district:',
    },
    'sainte-melanie-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2461050/district:',
    },
    'sainte-sophie-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2475028/district:',
    },
    'sainte-therese-de-gaspe-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2402010/district:',
    },
    'sainte-therese-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2473010/district:',
    },
    'salaberry-de-valleyfield-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2470052/district:',
    },
    'saskatchewan-electoral-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/province:sk/ed:',
    },
    'saskatchewan-electoral-districts-representation-act-2012': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/province:sk/ed:',
    },
    'saskatoon-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4711066/ward:',
    },
    'sault-ste-marie-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3557061/ward:',
    },
    'senneterre-quartiers': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2489040/quartier:',
    },
    'senneville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466127/district:',
    },
    'sept-iles-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2497007/district:',
    },
    'shawinigan-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2436033/district:',
    },
    'sherbrooke-boroughs': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2443027/borough:',
    },
    'sherbrooke-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2443027/district:',
    },
    'silverwood-no-123-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4705011/division:',
    },
    'sorel-tracy-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2453052/district:',
    },
    'south-quappelle-no-157-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4706034/division:',
    },
    'spiritwood-no-496-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4716056/division:',
    },
    'st-catharines-wards': {
        'boundary_key': matcher,
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3526053/ward:',
    },
    'st-johns-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1001519/ward:',
    },
    'stratford-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1102080/ward:',
    },
    'strathcona-county-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4811052/ward:',
    },
    'sud-ouest-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'summerside-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1103025/ward:',
    },
    'temiscouata-sur-le-lac-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2413073/district:',
    },
    'terrebonne-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2464008/district:',
    },
    'thetford-mines-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2431084/district:',
    },
    'thunder-bay-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3558004/ward:',
    },
    'tisdale-no-427-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4714043/division:',
    },
    'torch-river-no-488-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4714077/division:',
    },
    'toronto-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3520005/ward:',
    },
    'trois-pistoles-quartiers': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2411040/quartier:',
    },
    'trois-rivieres-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2437067/district:',
    },
    'upper-miramichi-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:1309027/ward:',
    },
    'val-david-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2478010/district:',
    },
    'val-des-monts-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2482015/district:',
    },
    'val-dor-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2489008/district:',
    },
    'vanscoy-no-345-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4712054/division:',
    },
    'varennes-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2459020/district:',
    },
    'vaudreuil-dorion-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2471083/district:',
    },
    'vaughan-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3519028/ward:',
    },
    'vercheres-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2459025/district:',
    },
    'verdun-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'victoriaville-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2439062/district:',
    },
    'ville-marie-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'villeraysaint-michelparc-extension-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466023/district:',
    },
    'waterloo-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2447025/district:',
    },
    'waterloo-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3530016/ward:',
    },
    'wawken-no-93-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4701076/division:',
    },
    'webb-no-138-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4708006/division:',
    },
    'weedon-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2441098/district:',
    },
    'welland-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3526032/ward:',
    },
    'wellesley-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3530027/ward:',
    },
    'wentworth-nord-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2477060/district:',
    },
    'westmount-districts': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:2466032/district:',
    },
    'whiska-creek-no-106-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4703059/division:',
    },
    'whitby-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3518009/ward:',
    },
    'willowdale-no-153-divisions': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4705033/division:',
    },
    'wilmot-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3530020/ward:',
    },
    'windsor-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3537039/ward:',
    },
    'winnipeg-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4611040/ward:',
    },
    'wood-buffalo-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:4816037/ward:',
    },
    'woolwich-wards': {
        'boundary_key': 'external_id',
        'key': 'id',
        'prefix': 'ocd-division/country:ca/csd:3530035/ward:',
    },
}
