"""End-to-end smoke test. Needs a database loaded via `python db_init.py`.

Run:  python tests/smoke_test.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app  # noqa: E402

app.config['TESTING'] = True
import uuid
EMAIL = f'smoke.{uuid.uuid4().hex[:8]}@example.com'
c = app.test_client()
failures = []


def check(label, resp, expect=(200, 302)):
    ok = resp.status_code in expect
    print(f"{'PASS' if ok else 'FAIL'}  {resp.status_code}  {label}")
    if not ok:
        failures.append(label)


for path in ['/', '/pets/', '/products/', '/pets/1', '/products/1', '/auth/login', '/auth/register', '/cart/']:
    check(f'GET {path}', c.get(path))

check('register', c.post('/auth/register', data=dict(
    first_name='Test', last_name='User', email=EMAIL, phone='6085550100',
    password='Sm0ke!Test', confirm_password='Sm0ke!Test')))
r = c.post('/auth/login', data=dict(email=EMAIL, password='Sm0ke!Test'))
check('login with hashed password', r)
with c.session_transaction() as s:
    if not s.get('logged_in'):
        failures.append('session not logged in'); print('FAIL  session not logged in')
check('add pet to cart', c.post('/cart/add', json={'id': 1, 'type': 'pet', 'quantity': 1}))
check('add product to cart', c.post('/cart/add', json={'id': 1, 'type': 'product', 'quantity': 2}))
check('view cart', c.get('/cart/'))
r = c.post('/cart/checkout', data=dict(payment_method='Credit Card', address_id='new', save_address='on',
    street1='1 Bascom Hill', city='Madison', state='WI', zip='53706'), follow_redirects=True)
check('place order', r, expect=(200,))
import re as _re
_m = _re.search(r'Order #(\d+)', r.get_data(as_text=True))
last_order_id = _m.group(1) if _m else None
if not last_order_id:
    failures.append('order detail page not shown'); print('FAIL  order detail page not shown')
orders = c.get('/user/orders').get_data(as_text=True)
if 'Order' not in orders:
    failures.append('order not listed'); print('FAIL  order not listed')
for path in ['/user/profile', '/user/addresses', '/user/orders', '/cart/checkout']:
    check(f'GET {path} (logged in)', c.get(path))

# admin flow (seed admin account from schema.sql)
a = app.test_client()
check('admin login', a.post('/admin/login', data=dict(email='gfilpi1@slashdot.org', password='oD1#qrLc(@')))
for path in ['/admin/', '/admin/pets', '/admin/products', '/admin/orders',
             '/admin/pets/add', '/admin/pets/edit/1', '/admin/products/add', '/admin/products/edit/1']:
    check(f'GET {path} (admin)', a.get(path), expect=(200,))
r = a.post('/admin/pets/add', data=dict(pet_name='Smokey', breed_id='1', age='2', price='199.99'), follow_redirects=True)
check('admin add pet', r, expect=(200,))
if 'Smokey' not in r.get_data(as_text=True):
    failures.append('new pet not listed'); print('FAIL  new pet not listed')
if last_order_id:
    check('GET admin order detail', a.get(f'/admin/orders/{last_order_id}'), expect=(200,))
    check('update order status', a.post(f'/admin/orders/update-status/{last_order_id}',
          data=dict(order_status='Processing', delivery_status='Shipped')))

print('\nAll checks passed' if not failures else f'\n{len(failures)} failure(s): {failures}')
sys.exit(1 if failures else 0)
