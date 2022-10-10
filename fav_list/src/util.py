def build_update_expression(data):
    pf = 'prefix'
    vals = {}
    exp = 'SET '
    attr_names = {}
    for key,value in data.items():
        vals[':{}'.format(key)] = {"S": value}
        attr_names['#pf_{}'.format(key)] = key
        exp += '#pf_{} = :{},'.format(key, key)
    exp = exp.rstrip(",")
    return vals, exp, attr_names