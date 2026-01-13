const db = require('../db');
const fs = require('fs');
const path = require('path');
const xlsx = require('xlsx');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

async function exportData() {
    console.log('Connecting to data source...');
    // We don't need to explicitly connect if we are just reading files, but for DB we do.
    // db.connect() handles the mode check.
    await db.connect();

    const schools = await db.getAllSchools();
    await db.close();

    if (!schools || schools.length === 0) {
        console.log('No data to export.');
        return;
    }

    console.log(`Exporting ${schools.length} records...`);

    // Prepare data for Excel/CSV
    // Map DB columns to friendly headers
    const data = schools.map(s => ({
        'Affiliation No': s.affiliation_number,
        'School Name': s.school_name,
        'Address': s.address,
        'City': s.city,
        'District': s.district,
        'State': s.state,
        'Pincode': s.pincode,
        'Phone': s.phone,
        'Email': s.email,
        'Website': s.website,
        'Source': s.source,
        'Confidence': s.email_confidence
    }));

    const outputDir = path.join(__dirname, '../data_output');
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    // Export CSV
    try {
        const csvPath = path.join(outputDir, 'schools.csv');
        const csvWriter = createCsvWriter({
            path: csvPath,
            header: Object.keys(data[0]).map(id => ({id, title: id}))
        });

        // CSV Writer expects keys to match IDs. The keys in 'data' objects are the headers themselves in this case.
        // We need to map data to keys that match the header IDs.
        // Actually, since we used friendly names as keys in `data`, we can use those.

        await csvWriter.writeRecords(data);
        console.log(`Exported CSV to ${csvPath}`);
    } catch (e) {
        console.error('Error exporting CSV:', e.message);
    }

    // Export Excel
    try {
        const wb = xlsx.utils.book_new();
        const ws = xlsx.utils.json_to_sheet(data);
        xlsx.utils.book_append_sheet(wb, ws, 'Schools');
        const xlsxPath = path.join(outputDir, 'schools.xlsx');
        xlsx.writeFile(wb, xlsxPath);
        console.log(`Exported Excel to ${xlsxPath}`);
    } catch (e) {
        console.error('Error exporting Excel:', e.message);
    }
}

if (require.main === module) {
    exportData();
}

module.exports = { exportData };
