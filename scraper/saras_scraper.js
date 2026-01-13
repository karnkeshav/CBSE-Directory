const { chromium } = require('playwright');
const db = require('../db');
require('dotenv').config();

// Use file storage by default in this environment if DB is not set
if (!process.env.DATABASE_URL) {
    process.env.SAVE_TO_FILE = 'true';
}

const TARGET_STATE = 'TELANGANA';
const TARGET_DISTRICTS = ['HYDERABAD', 'RANGAREDDY', 'MEDCHAL-MALKAJGIRI', 'SANGAREDDY'];
// Note: Medchal-Malkajgiri might be spelled differently in dropdown, we need to handle that.
// The snippet showed "MEDCHAL" or similar might be there.

async function scrapeSaras() {
    await db.connect();

    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();

    try {
        console.log('Navigating to CBSE SARAS...');
        await page.goto('https://saras.cbse.gov.in/saras/AffiliatedList/ListOfSchdirReportNew');

        // Select "State wise" radio button
        // Based on snippet: "( ) State wise"
        // We need to find the radio button. It might have an ID or name.
        // Let's try to click by label.
        await page.getByLabel('State wise').check();

        // Wait for State dropdown to be enabled/populated
        // The snippet shows "State [--select--__________]"
        await page.waitForTimeout(2000); // Wait for potential AJAX

        // Select State
        console.log(`Selecting state: ${TARGET_STATE}`);
        // The dropdown ID might be 'ddlState' or similar. We'll try by Label or select option.
        // If "State" is the label text
        // Note: The value might be '26' or '36' (Telangana code). We should select by label.
        // We need to find the select element.
        const stateSelect = page.locator('select').filter({ hasText: 'Select State' }).or(page.locator('#ddlState'));
        // We'll try a generic approach if ID is unknown, but usually it's ddlState or State.

        // Let's assume standard ASP.NET IDs: ddlState, ddlDistrict
        // Or inspect the select options if possible.
        // Since I can't interactively inspect, I'll try to select by text "TELANGANA".

        // Trying to find the select element near "State" text
        await page.selectOption('select[id*="State"]', { label: TARGET_STATE }).catch(async () => {
             // Fallback: try to find any select that has TELANGANA
             await page.locator('select').filter({ hasText: TARGET_STATE }).first().selectOption({ label: TARGET_STATE });
        });

        await page.waitForTimeout(2000); // Wait for districts to load

        for (const district of TARGET_DISTRICTS) {
            console.log(`Processing District: ${district}`);

            // Handle district name variations if needed
            // e.g., Medchal might be separate

            try {
                // Select District
                await page.selectOption('select[id*="District"]', { label: district });
            } catch (e) {
                console.log(`Could not select district ${district} directly. Trying partial match...`);
                // Get all options
                const options = await page.locator('select[id*="District"] option').allInnerTexts();
                const match = options.find(opt => opt.toUpperCase().includes(district) || district.includes(opt.toUpperCase()));
                if (match) {
                    console.log(`Found matching district: ${match}`);
                    await page.selectOption('select[id*="District"]', { label: match });
                } else {
                    console.error(`District ${district} not found.`);
                    continue;
                }
            }

            // Click Search
            await page.click('input[type="submit"][value="Search"], button:has-text("Search")');

            await page.waitForLoadState('networkidle');
            await page.waitForTimeout(2000);

            // Scrape the table
            await scrapeTable(page);

            // Go back or reset?
            // "Back to Home" link or just re-select.
            // It seems the search results replace the form or appear below.
            // If they replace, we need to go back.
            // If they appear below, we just select next district.

            // Check if search form is still visible
            const isSearchVisible = await page.isVisible('select[id*="District"]');
            if (!isSearchVisible) {
                await page.goBack();
                await page.waitForTimeout(1000);
            }
        }

    } catch (error) {
        console.error('Error during scraping:', error);
        // Take screenshot
        await page.screenshot({ path: 'error_screenshot.png' });
    } finally {
        await browser.close();
        await db.close();
    }
}

async function scrapeTable(page) {
    // Determine number of pages or rows
    // The snippet shows "Show 10, 25, 50, 100 entries" and "Search: ..."
    // It's a DataTable.

    // We should try to show "All" or "100" entries to minimize pagination.
    try {
        await page.selectOption('select[name*="length"]', { value: '100' }); // Try to select 100
        await page.waitForTimeout(1000);
    } catch (e) {
        // Ignore if not present
    }

    let hasNext = true;
    while (hasNext) {
        const rows = page.locator('table tbody tr');
        const count = await rows.count();
        console.log(`Found ${count} schools on this page.`);

        for (let i = 0; i < count; i++) {
            const row = rows.nth(i);
            const cells = row.locator('td');

            // Columns based on snippet: S No, Reg No., State, District, Status, School Name, Affiliation Status, Region, Details
            // Indexes: 0: SNo, 1: RegNo, 2: State, 3: District, 4: Status, 5: Name, 6: Aff Status, 7: Region, 8: Details (View link)

            // Ensure row is valid
            if (await cells.count() < 8) continue;

            const affNo = await cells.nth(1).innerText();
            const state = await cells.nth(2).innerText();
            const district = await cells.nth(3).innerText();
            const schoolName = await cells.nth(5).innerText();
            const region = await cells.nth(7).innerText();

            const schoolData = {
                affiliation_number: affNo.trim(),
                school_name: schoolName.trim(),
                state: state.trim(),
                district: district.trim(),
                source: 'saras'
            };

            // Get Details link
            const viewLink = row.locator('a:has-text("View")');
            if (await viewLink.count() > 0) {
                 // We can open in new tab or click and go back.
                 // Better to get the href and visit separately to avoid losing state?
                 // But the href might be javascript:__doPostBack.
                 // If it is a real link, we can visit.
                 // Snippet: [5]View -> https://saras.cbse.gov.in/saras/AffiliatedList/AfflicationDetails/1000029
                 // It looks like a clean URL.

                 const href = await viewLink.getAttribute('href');
                 if (href) {
                     const detailUrl = href.startsWith('http') ? href : `https://saras.cbse.gov.in${href}`;
                     console.log(`Fetching details for ${schoolName} from ${detailUrl}`);

                     // Use a separate page for details to keep the list page intact
                     const detailPage = await page.context().newPage();
                     try {
                         await detailPage.goto(detailUrl, { timeout: 30000 });
                         const details = await scrapeDetails(detailPage);
                         Object.assign(schoolData, details);
                     } catch (err) {
                         console.error(`Failed to scrape details for ${schoolName}:`, err);
                     } finally {
                         await detailPage.close();
                     }
                 }
            }

            await db.upsertSchool(schoolData);

            // Rate limiting
            await new Promise(r => setTimeout(r, 1000 + Math.random() * 1000));
        }

        // Check for "Next" button
        const nextBtn = page.locator('a.paginate_button.next:not(.disabled)');
        if (await nextBtn.isVisible()) {
            await nextBtn.click();
            await page.waitForTimeout(2000);
        } else {
            hasNext = false;
        }
    }
}

async function scrapeDetails(page) {
    // Scrape Address, Phone, Email, Website, Pincode
    // We need to inspect the details page structure.
    // Assuming standard layout (often tables or div grids).
    // We'll extract all text and use Regex or try to find specific labels.

    const bodyText = await page.innerText('body');

    const emailMatch = bodyText.match(/Email\s*[:\-]?\s*([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+)/i);
    const phoneMatch = bodyText.match(/Phone\s*[:\-]?\s*([\d\s\-]+)/i);
    const websiteMatch = bodyText.match(/Website\s*[:\-]?\s*(https?:\/\/[^\s]+|www\.[^\s]+)/i);
    const addressMatch = bodyText.match(/Address\s*[:\-]?\s*([\s\S]*?)(\n|$|Pin)/i);
    const pincodeMatch = bodyText.match(/Pincode\s*[:\-]?\s*(\d{6})/i);
    const cityMatch = bodyText.match(/City\s*[:\-]?\s*([^\n\r]+)/i);

    return {
        email: emailMatch ? emailMatch[1] : null,
        phone: phoneMatch ? phoneMatch[1].trim() : null,
        website: websiteMatch ? websiteMatch[1] : null,
        address: addressMatch ? addressMatch[1].trim() : null,
        pincode: pincodeMatch ? pincodeMatch[1] : null,
        city: cityMatch ? cityMatch[1].trim() : null
    };
}

if (require.main === module) {
    scrapeSaras();
}

module.exports = { scrapeSaras };
