const { Client } = require('pg');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

// Determine mode based on env var, but allow dynamic fallback
let saveToFile = process.env.SAVE_TO_FILE === 'true';
const DATA_DIR = path.join(__dirname, '../data_output');

// Ensure directory exists if we might write to it
if (saveToFile && !fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

const client = new Client({
    connectionString: process.env.DATABASE_URL,
});

async function connect() {
    if (!saveToFile) {
        try {
            await client.connect();
            console.log('Connected to PostgreSQL');
        } catch (err) {
            console.error('Failed to connect to PostgreSQL, falling back to file storage', err.message);
            // Fallback to file mode
            saveToFile = true;
            process.env.SAVE_TO_FILE = 'true';

            // Ensure dir exists now that we switched modes
            if (!fs.existsSync(DATA_DIR)) {
                fs.mkdirSync(DATA_DIR, { recursive: true });
            }
        }
    }
}

async function upsertSchool(schoolData) {
    if (saveToFile) {
        const filePath = path.join(DATA_DIR, 'schools.json');
        let schools = [];
        if (fs.existsSync(filePath)) {
            try {
                schools = JSON.parse(fs.readFileSync(filePath, 'utf8'));
            } catch (e) {
                schools = [];
            }
        }

        const index = schools.findIndex(s => s.affiliation_number === schoolData.affiliation_number);
        if (index >= 0) {
            schools[index] = { ...schools[index], ...schoolData, updated_at: new Date().toISOString() };
        } else {
            schools.push({ ...schoolData, created_at: new Date().toISOString() });
        }

        fs.writeFileSync(filePath, JSON.stringify(schools, null, 2));
        console.log(`Saved school ${schoolData.affiliation_number} to file`);
        return;
    }

    const query = `
        INSERT INTO schools (
            affiliation_number, school_name, address, city, district, state, pincode,
            phone, email, website, source, last_scraped_at
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, NOW()
        ) ON CONFLICT (affiliation_number) DO UPDATE SET
            school_name = EXCLUDED.school_name,
            address = EXCLUDED.address,
            city = EXCLUDED.city,
            district = EXCLUDED.district,
            state = EXCLUDED.state,
            pincode = EXCLUDED.pincode,
            phone = EXCLUDED.phone,
            email = EXCLUDED.email,
            website = EXCLUDED.website,
            source = EXCLUDED.source,
            last_scraped_at = NOW();
    `;

    const values = [
        schoolData.affiliation_number,
        schoolData.school_name,
        schoolData.address,
        schoolData.city,
        schoolData.district,
        schoolData.state,
        schoolData.pincode,
        schoolData.phone,
        schoolData.email,
        schoolData.website,
        schoolData.source || 'saras'
    ];

    try {
        await client.query(query, values);
        console.log(`Upserted school ${schoolData.affiliation_number} to DB`);
    } catch (err) {
        console.error('Error upserting school:', err.message);
    }
}

async function getSchoolsWithoutEmail() {
    if (saveToFile) {
         const filePath = path.join(DATA_DIR, 'schools.json');
         if (!fs.existsSync(filePath)) return [];
         const schools = JSON.parse(fs.readFileSync(filePath, 'utf8'));
         return schools.filter(s => !s.email);
    }

    const res = await client.query("SELECT * FROM schools WHERE email IS NULL OR email = ''");
    return res.rows;
}

async function getAllSchools() {
    if (saveToFile) {
        const filePath = path.join(DATA_DIR, 'schools.json');
        if (!fs.existsSync(filePath)) return [];
        return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }

    const res = await client.query("SELECT * FROM schools");
    return res.rows;
}

async function close() {
    if (!saveToFile) {
        await client.end();
    }
}

module.exports = {
    connect,
    upsertSchool,
    getSchoolsWithoutEmail,
    getAllSchools,
    close,
    client // Export client just in case, but prefer using helper methods
};
