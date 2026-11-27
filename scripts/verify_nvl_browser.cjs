const { chromium } = require('playwright');
const assert = require('node:assert/strict');
(async()=>{
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
try {
const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.route('https://**/*',async route=>{
 if(route.request().url().includes('chart.js@4.4.8')) return route.fulfill({path:require('node:path').join(require('node:path').dirname(require.resolve('chart.js')),'chart.umd.js'),contentType:'application/javascript'});
 return route.abort();
});
await page.goto('http://127.0.0.1:8765/#co-phieu',{waitUntil:'domcontentloaded'});
await page.locator('#stockSymbol').selectOption('NVL');
await page.waitForFunction(()=>document.querySelector('#stockStatementHead')?.textContent.includes('Q3/2026')&&document.querySelector('#stockStatementHead')?.textContent.includes('Q1/2025'));
await page.locator('#stockUnit').selectOption('billion');
const cell=async(label,period)=>{
 const headers=await page.locator('#stockStatementHead th').allTextContents();
 const col=headers.findIndex(h=>h.includes(period));assert(col>0,period);
 const row=page.locator('#stockTableBody tr').filter({has:page.locator('td.statement-row-label',{hasText:label})}).first();
 return (await row.locator('td').nth(col).innerText()).trim();
};
await page.locator('[data-statement="balance"]').click();
assert.match(await cell(/^Tổng cộng tài sản$/i,'Q3/2026'),/258,814.8/);
await page.locator('[data-statement="income"]').click();
assert.equal(await cell(/^Giá vốn hàng bán$/,'Q4/2025'),'1,015.2');
await page.locator('[data-statement="cashflow"]').click();
await page.locator('#stockCashflowBasis').selectOption('quarter');
assert.equal(await cell(/^Lưu chuyển tiền thuần từ hoạt động kinh doanh$/,'Q2/2026'),'-3,175.2');
assert.equal(await cell(/^Lưu chuyển tiền thuần từ hoạt động đầu tư$/,'Q2/2026'),'5,021.1');
assert.equal(await cell(/^Lưu chuyển tiền thuần từ hoạt động tài chính$/,'Q2/2026'),'-1,346.6');
assert.equal(await cell(/^Điều chỉnh cơ sở trình bày/,'Q2/2026'),'-45.6');
await page.screenshot({path:'nvl-quarter-browser.png',fullPage:true});
await page.locator('#stockCashflowBasis').selectOption('ytd');
assert.equal(await page.locator('#stockTableBody td.statement-row-label').filter({hasText:'Điều chỉnh cơ sở trình bày'}).count(),0);
assert.equal(await cell(/^Lưu chuyển tiền thuần từ hoạt động kinh doanh$/,'Q2/2026'),'-3,611.7');
await page.locator('[data-statement="ratios"]').click();
assert.match(await cell(/^ROA/,'Q3/2026'),/1.7/);
assert.match(await cell(/^ROE/,'Q3/2026'),/6.7/);
assert.deepEqual(errors,[]);
console.log('NVL browser acceptance checks passed');
}catch(e){
 console.error('DOM headers:',await page.locator('#stockStatementHead').innerText().catch(()=>''));
 console.error('DOM row labels:',await page.locator('#stockTableBody td.statement-row-label').allTextContents().catch(()=>[]));
 await page.screenshot({path:'nvl-quarter-browser.png',fullPage:true}).catch(()=>{});
 throw e;
}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
