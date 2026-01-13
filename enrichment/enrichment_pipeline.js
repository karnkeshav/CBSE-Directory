const db = require('../db');
const { chromium } = require('playwright');
const axios = require('axios');
const dns = require('dns').promises;

// Pass 2: School Website Scraping
async function enrichEmails() {
    await db.connect();

    // Get schools with missing emails
    const schools = await db.getSchoolsWithoutEmail();
    console.log(`Found ${schools.length} schools needing email enrichment.`);

    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();

    for (const school of schools) {
        if (!school.website) {
            // Pass 3: Google Maps API (Fallback)
            console.log(`No website for ${school.school_name}, attempting Google Maps API...`);
            const foundWebsite = await searchGoogleMapsAPI(school);
            if (foundWebsite) {
                school.website = foundWebsite;
                await db.upsertSchool(school); // Update website found
            } else {
                console.log(`Could not find website for ${school.school_name}`);
                continue;
            }
        }

        if (school.website) {
             console.log(`Scraping website ${school.website} for ${school.school_name}...`);
             const email = await scrapeWebsiteForEmail(context, school.website);
             if (email) {
                 // Validate Email
                 const isValid = await validateEmail(email);
                 if (isValid) {
                     console.log(`Found and validated email ${email} for ${school.school_name}`);
                     school.email = email;
                     school.email_confidence = 'MEDIUM'; // Website source
                     await db.upsertSchool(school);
                 } else {
                     console.log(`Email ${email} failed validation.`);
                 }
             } else {
                 console.log(`No email found on website for ${school.school_name}`);
             }
        }

        // Rate limit
        await new Promise(r => setTimeout(r, 1000));
    }

    await browser.close();
    await db.close();
}

async function scrapeWebsiteForEmail(context, url) {
    const page = await context.newPage();
    let email = null;
    try {
        if (!url.startsWith('http')) url = 'http://' + url;
        await page.goto(url, { timeout: 15000, waitUntil: 'domcontentloaded' });

        // Strategy 1: Look for mailto links
        const mailto = await page.getAttribute('a[href^="mailto:"]', 'href');
        if (mailto) {
            return mailto.replace('mailto:', '').trim();
        }

        // Strategy 2: Regex on body text
        const bodyText = await page.innerText('body');
        const emailRegex = /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+)/gi;
        const matches = bodyText.match(emailRegex);
        if (matches && matches.length > 0) {
            // Filter out image extensions or invalid ones
            const valid = matches.filter(e => !e.match(/\.(png|jpg|jpeg|gif|css|js)$/i));
            // Prioritize info, office, principal
            const priority = valid.find(e => /info|office|principal|contact|admin/i.test(e));
            return priority || valid[0];
        }

        // Strategy 3: Check /contact page
        const contactLink = await page.getByText(/contact|reach us/i).first();
        if (await contactLink.isVisible()) {
             await contactLink.click();
             await page.waitForTimeout(2000);
             const contactBody = await page.innerText('body');
             const contactMatches = contactBody.match(emailRegex);
             if (contactMatches && contactMatches.length > 0) {
                 return contactMatches[0];
             }
        }

    } catch (e) {
        // console.error(`Error scraping ${url}:`, e.message);
    } finally {
        await page.close();
    }
    return email;
}

async function searchGoogleMapsAPI(school) {
    const apiKey = process.env.GOOGLE_MAPS_API_KEY;
    if (!apiKey) {
        console.log("Skipping Google Maps API (No Key provided)");
        return null;
    }

    try {
        // Text Search API
        const query = `${school.school_name} ${school.city || school.district}`;
        const url = `https://maps.googleapis.com/maps/api/place/textsearch/json?query=${encodeURIComponent(query)}&key=${apiKey}`;

        const response = await axios.get(url);
        if (response.data.results && response.data.results.length > 0) {
            const placeId = response.data.results[0].place_id;

            // Get Place Details to retrieve website
            const detailsUrl = `https://maps.googleapis.com/maps/api/place/details/json?place_id=${placeId}&fields=website&key=${apiKey}`;
            const detailsResponse = await axios.get(detailsUrl);

            if (detailsResponse.data.result && detailsResponse.data.result.website) {
                return detailsResponse.data.result.website;
            }
        }
    } catch (error) {
        console.error("Google Maps API Error:", error.message);
    }
    return null;
}

async function validateEmail(email) {
    // 1. Regex Validation
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regex.test(email)) return false;

    // 2. MX Record Check
    const domain = email.split('@')[1];
    try {
        const mxRecords = await dns.resolveMx(domain);
        if (mxRecords && mxRecords.length > 0) {
            return true;
        }
    } catch (e) {
        console.log(`MX Check failed for ${domain}: ${e.message}`);
    }
    return false;
}

if (require.main === module) {
    enrichEmails();
}

module.exports = { enrichEmails };
