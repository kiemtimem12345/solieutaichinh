// Execute actual dashboard calculation fragments against checked-in financial snapshots.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const js = fs.readFileSync('assets/app.js','utf8');
const rows = JSON.parse(fs.readFileSync('data/financials-NVL.json','utf8')).items;
const q2 = rows.find(r=>r.period==='2026-Q2');
const q4 = rows.find(r=>r.period==='2025-Q4');
function fragment(start,end) {
  const a=js.indexOf(start), b=js.indexOf(end,a);
  assert(a>=0 && b>a, 'missing production code anchor '+start);
  return js.slice(a,b);
}
const context=vm.createContext({rows,q2,q4, cashflowBasisSelect:{value:'quarter'}, validNumber:v=>v!==null&&v!==undefined&&v!==''&&Number.isFinite(Number(v)), resolveStatementValue:(row,key)=>({value:row[key]??null})});
vm.runInContext(fragment('const cashflowValue = ','const displayPeriod = ')+';globalThis.calc=cashflowValue;',context);
const calc=(row,field)=>context.calc(row,field,rows,'NVL');
const vnd=x=>Math.round(x*1e6);
assert.equal(vnd(calc(q2,'cash_opening_basis_adjustment')),-45552261468);
assert.equal(vnd(calc(q2,'foreign_exchange_effect')),171153);
assert.equal(vnd(calc(q2,'net_cash_change')),499330659820);
assert.equal(vnd(calc(q2,'cash_beginning')),4518328920108);
assert.equal(vnd(calc(q2,'cash_ending')),4972107489613);
assert.equal(calc({...q2,cashflow_period_basis:'quarter'},'cash_opening_basis_adjustment'),null);
assert.equal(calc(q4,'cash_opening_basis_adjustment'),null);
context.cashflowBasisSelect.value='ytd';
assert.equal(calc(q2,'cash_opening_basis_adjustment'),null);
assert.equal(vnd(calc(q2,'cash_beginning')),4352030381743);
assert.equal(vnd(calc(q2,'foreign_exchange_effect')),917501);
assert.equal(vnd(calc(q2,'net_cash_change')),620076190369);
const credit=fragment('const preserveSourceCredit = ','const displayed = ');
vm.runInContext('globalThis.expense=(item,def,resolvedValue)=>{'+credit+'return displayValue;};',context);
const def={key:'cost_of_goods_sold',negativeExpense:true};
assert.equal(vnd(context.expense(q4,def,q4.cost_of_goods_sold)),1015177327509);
assert.equal(vnd(context.expense({...q4,source_validation:{}},def,q4.cost_of_goods_sold)),-1015177327509);
assert.equal(vnd(context.expense({...q4,gross_profit:q4.gross_profit+1},def,q4.cost_of_goods_sold)),-1015177327509);
assert.equal(context.expense(q2,def,q2.cost_of_goods_sold),q2.cost_of_goods_sold);
console.log('NVL 15 runtime calculation checks passed (isolated actual dashboard fragments, not full browser DOM).');
