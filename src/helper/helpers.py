import copy

from src.master.models import Condition

def setDefaultValue(field, data, default):
    return data[field] if field in data and data[field] != None else default

def compareDict(dict1, dict2, output, parent=None):
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        d1_keys = dict1.keys()
        d2_keys = dict2.keys()
        intersect_keys = set(d1_keys).intersection(set(d2_keys))
        for i in intersect_keys:

            txtparent = ''
            if parent:
                txtparent = parent + '__'

            if dict1[i] != dict2[i] :
                if (isinstance(dict1[i], dict) and isinstance(dict2[i], dict)) or \
                        (isinstance(dict1[i], list) and isinstance(dict2[i], list)) :
                    compareDict(dict1[i], dict2[i], output, i)
                else:
                    modified = {
                        'attr': txtparent + i,
                        'old': dict1[i],
                        'new': dict2[i]
                    }
                    output.append(modified)
    else:
        txtparent = ''
        if parent:
            txtparent = parent + '__'

        if parent == 'durations':
            val = {
                'old' : {
                    'day': [],
                    'hour': []
                },
                'new': {
                    'day': [],
                    'hour': []
                }
            }
            for i in dict1:
                if 'duration_type' in i:
                    if i['duration_type'] == 'DAY':
                        val['old']['day'].append(i['values'])

                    if i['duration_type'] == 'HOUR':
                        val['old']['hour'].append(i['values'])


            for i in dict2:
                if 'duration_type' in i:
                    if i['duration_type'] == 'DAY':
                        val['new']['day'].append(i['values'])

                    if i['duration_type'] == 'HOUR':
                        val['new']['hour'].append(i['values'])

            output.append(
                {
                    'attr': txtparent + 'DAY',
                    'old' : ', '.join(map(str, val['old']['day'])) if len(val['old']['day']) > 0 else val['old']['day'],
                    'new' : ', '.join(map(str, val['new']['day'])) if len(val['new']['day']) > 0 else val['new']['day']
                }
            )

            output.append(
                {
                    'attr': txtparent + 'HOUR',
                    'old': ', '.join(map(str, val['old']['hour'])) if len(val['old']['hour']) > 0 else val['old']['hour'],
                    'new': ', '.join(map(str, val['new']['hour'])) if len(val['new']['hour']) > 0 else val['new']['hour']
                }
            )

        elif parent == 'conditions':

            for i in Condition.objects.all():

                val_old = None
                for z in dict1:
                    if z['code'] == i.code:
                        old = ', '.join(map(str, z['values_text']))
                        val_old = {'val': z['operator_text'] + ' ' + old}
                        val_old['attr'] = z['name']


                val_new = None
                for z in dict2:
                    if z['code'] == i.code:
                        new = ', '.join(map(str, z['values_text']))
                        val_new = {'val': z['operator_text'] + ' ' + new}
                        val_new['attr'] = z['name']



                modified = {
                    'attr': txtparent + i.name,
                    'old': val_old['val'] if val_old else None,
                    'new': val_new['val'] if val_new else None
                }

                if val_old or val_new:
                    output.append(modified)

        else:
            val = {
                'attr': parent,
                'old': ', '.join(map(str, dict1)),
                'new': ', '.join(map(str, dict2))
            }

            output.append(val)