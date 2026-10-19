import unittest
from rup_proof_trace import verify,parse_cnf
CNF='p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n'
class Behavior(unittest.TestCase):
 def test_verified_reasons(self):
  r=verify(CNF,'1 0\n0\n');self.assertEqual(r['status'],'verified')
  self.assertEqual(r['steps'][0]['assumptions'],[-1]);self.assertEqual(r['steps'][0]['implied'][0],dict(literal=2,reason_id=1))
  self.assertEqual(r['steps'][0]['conflict']['id'],2)
 def test_missing_empty(self):self.assertEqual(verify(CNF,'1 0')['status'],'incomplete')
 def test_not_rup(self):self.assertEqual(verify('p cnf 2 1\n1 2 0','-1 0')['status'],'not_rup')
 def test_empty_formula_clause(self):self.assertEqual(verify('p cnf 0 1\n0','0')['status'],'verified')
 def test_tautology(self):self.assertEqual(verify('p cnf 1 0','1 -1 0')['steps'][0]['conflict']['kind'],'contradictory_assumptions')
 def test_unit_deletion_applies(self):
  self.assertEqual(verify('p cnf 1 2\n1 0\n-1 0','d 1 0\n0')['status'],'not_rup')
 def test_duplicate_multiset(self):
  r=verify('p cnf 1 3\n1 0\n1 0\n-1 0','d 1 0\n0');self.assertEqual(r['status'],'verified');self.assertEqual(r['steps'][0]['delete_id'],1)
 def test_delete_absent(self):
  with self.assertRaisesRegex(ValueError,'absent'):verify('p cnf 1 0','d 1 0')
 def test_final_empty(self):
  with self.assertRaisesRegex(ValueError,'final'):verify('p cnf 0 1\n0','0\n0')
 def test_parser_boundaries(self):
  for s in ('p cnf 1 1\n2 0','p cnf 1 2\n1 0','p cnf 1 1\n1','1 0','p cnf 65 0'):
   with self.assertRaises(ValueError):parse_cnf(s)
 def test_multiline_comments(self):self.assertEqual(parse_cnf('c example\np cnf 2 1\n1\nc gap\n2 0')[1],[(1,2)])
 def test_visit_budget(self):
  with self.assertRaisesRegex(ValueError,'budget'):verify(CNF,'1 0\n0',1)
