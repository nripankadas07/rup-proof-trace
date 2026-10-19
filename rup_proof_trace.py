"""Explain bounded reverse-unit-propagation proofs; not a full DRAT checker."""
import argparse
import hashlib
import json
import re
import sys


def clause(tokens, n):
    if any(not re.fullmatch(r'-?[0-9]+', t) for t in tokens):
        raise ValueError('non-DIMACS numeric token')
    try: values=[int(t) for t in tokens]
    except ValueError: raise ValueError('noninteger clause literal') from None
    if not values or values[-1] != 0 or 0 in values[:-1] or any(abs(v)>n for v in values[:-1]):
        raise ValueError('invalid clause terminator or variable')
    return tuple(sorted(set(values[:-1]), key=lambda x:(abs(x),x)))


def parse_cnf(text):
    header=None; tokens=[]
    for line in text.splitlines():
        s=line.strip()
        if not s or s.startswith('c'): continue
        if s.startswith('p'):
            p=s.split()
            if header is not None or tokens or len(p)!=4 or p[:2]!=['p','cnf']:
                raise ValueError('invalid DIMACS header')
            if any(not re.fullmatch(r'[0-9]+', t) for t in p[2:]):raise ValueError('non-DIMACS header count')
            try: n,m=map(int,p[2:])
            except ValueError: raise ValueError('invalid DIMACS counts') from None
            if not 0<=n<=64 or not 0<=m<=256: raise ValueError('CNF count limit')
            header=n,m
        else:
            if header is None: raise ValueError('header required before clauses')
            tokens.extend(s.split())
    if header is None: raise ValueError('missing DIMACS header')
    result=[]; start=0
    for i,t in enumerate(tokens):
        if t=='0': result.append(clause(tokens[start:i+1],header[0])); start=i+1
    if start!=len(tokens) or len(result)!=header[1]: raise ValueError('clause count/termination mismatch')
    return header[0],result


def verify(cnf, proof, budget=2000000):
    if type(budget) is not int or not 1<=budget<=2000000: raise ValueError('literal-visit budget limit')
    if len(cnf)+len(proof)>1048576 or not cnf.isascii() or not proof.isascii():
        raise ValueError('ASCII inputs combined at most 1 MiB')
    n,initial=parse_cnf(cnf)
    active={i+1:c for i,c in enumerate(initial)}; next_id=len(active)+1
    steps=[]; visits=0; completed=False
    lines=[s.strip() for s in proof.splitlines() if s.strip() and not s.strip().startswith('c')]
    if len(lines)>512: raise ValueError('at most 512 proof steps')
    for step,line in enumerate(lines,1):
        if completed: raise ValueError('empty clause must be the final proof step')
        ts=line.split(); deletion=ts[0]=='d'; c=clause(ts[1:] if deletion else ts,n)
        if deletion:
            match=next((i for i,v in active.items() if v==c),None)
            if match is None: raise ValueError('deletion of absent clause')
            del active[match]; steps.append({'step':step,'delete_id':match}); continue
        assigned={}; assumptions=[]; implied=[]; conflict=None
        for lit in c:
            value=lit<0; var=abs(lit)
            if var in assigned and assigned[var]!=value:
                conflict={'kind':'contradictory_assumptions'}; break
            assigned[var]=value; assumptions.append(-lit)
        changed=True
        while conflict is None and changed:
            changed=False
            for cid,existing in active.items():
                unknown=[]; satisfied=False
                for lit in existing:
                    visits+=1
                    if visits>budget: raise ValueError('literal-visit budget exceeded')
                    value=assigned.get(abs(lit))
                    if value is None: unknown.append(lit)
                    elif value==(lit>0): satisfied=True; break
                if satisfied: continue
                if not unknown: conflict={'kind':'clause','id':cid}; break
                if len(unknown)==1:
                    lit=unknown[0]; assigned[abs(lit)]=lit>0
                    implied.append({'literal':lit,'reason_id':cid}); changed=True
        record={'step':step,'clause':list(c),'assumptions':assumptions,'implied':implied,'conflict':conflict}
        steps.append(record)
        if conflict is None:
            return {'status':'not_rup','rejected_step':step,'steps':steps,'literal_visits':visits}
        record['added_id']=next_id; active[next_id]=c; next_id+=1
        if not c: completed=True
    return {'status':'verified' if completed else 'incomplete','steps':steps,'literal_visits':visits,
            'cnf_sha256':hashlib.sha256(cnf.encode('ascii')).hexdigest(),
            'proof_sha256':hashlib.sha256(proof.encode('ascii')).hexdigest()}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('cnf');p.add_argument('proof')
    p.add_argument('--budget',type=int,default=2000000);a=p.parse_args()
    try:
        def read(path):
            with open(path,'rb') as f: b=f.read(1048577)
            if len(b)>1048576: raise ValueError('input exceeds 1 MiB')
            return b.decode('ascii')
        r=verify(read(a.cnf),read(a.proof),a.budget)
        print(json.dumps(r,indent=2));return 0 if r['status']=='verified' else 1
    except (ValueError,UnicodeError,OSError) as e:
        print(str(e),file=sys.stderr);return 2


if __name__=='__main__':sys.exit(main())
