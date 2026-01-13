const { scrapeSaras } = require('./scraper/saras_scraper');
const { enrichEmails } = require('./enrichment/enrichment_pipeline');
const { exportData } = require('./utils/export');
const db = require('./db');

const command = process.argv[2];

(async () => {
    switch (command) {
        case 'scrape':
            console.log('Starting Scraper...');
            await scrapeSaras();
            break;
        case 'enrich':
            console.log('Starting Enrichment...');
            await enrichEmails();
            break;
        case 'export':
            console.log('Starting Export...');
            await exportData();
            break;
        case 'all':
            console.log('Running Full Pipeline...');
            await scrapeSaras();
            await enrichEmails();
            await exportData();
            break;
        default:
            console.log('Usage: node main.js [scrape|enrich|export|all]');
    }
})();
