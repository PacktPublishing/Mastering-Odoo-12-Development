from odoo import api
import time

for j in range(10):
    test_env = api.Environment(env.cr, 2, {})
    test_fields = ['name', 'email', 'phone', 'country_id']
    start = time.time()
    # read all fields in the current user to set data in cache
    test_env['res.users'].search_read([('id', '=', 2)], fields=[])
    for i in range(1000):
        [test_env.user[f] for f in test_fields]
    stop = time.time()
    test_env.clear()
    print('reading 4 fields 1000 times with cache: %1.4fs' % (stop-start,))

    # read 4 fields in db
    start = time.time()
    for i in range(1000):
        test_env['res.users'].search_read([('id', '=', 2)], fields=test_fields)
    test_env.clear()
    stop = time.time()
    print('reading 4 fields 1000 times without cache: %1.4fs' % (stop-start,))
