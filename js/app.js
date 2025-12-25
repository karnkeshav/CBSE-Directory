document.addEventListener('DOMContentLoaded', () => {
    const app = document.getElementById('app');
    const homeLink = document.getElementById('home-link');
    const trustsLink = document.getElementById('trusts-link');

    let schoolsData = {};
    let trustsData = [];

    // Fetch Data
    async function loadData() {
        try {
            const [schoolsRes, trustsRes] = await Promise.all([
                fetch('data/schools.json'),
                fetch('data/trusts.json')
            ]);
            schoolsData = await schoolsRes.json();
            trustsData = await trustsRes.json();
            renderStates();
        } catch (error) {
            console.error('Error loading data:', error);
            app.innerHTML = '<p>Error loading data. Please try again later.</p>';
        }
    }

    // Navigation
    homeLink.addEventListener('click', (e) => {
        e.preventDefault();
        renderStates();
    });

    trustsLink.addEventListener('click', (e) => {
        e.preventDefault();
        renderTrusts();
    });

    // Views
    function renderStates() {
        app.innerHTML = `
            <h2 class="view-title">Select a State</h2>
            <div class="grid-container" id="states-grid"></div>
        `;
        const grid = document.getElementById('states-grid');

        Object.keys(schoolsData).sort().forEach(state => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `<h3>${state}</h3>`;
            card.addEventListener('click', () => renderDistricts(state));
            grid.appendChild(card);
        });
    }

    function renderDistricts(state) {
        app.innerHTML = `
            <button class="back-btn" id="back-to-states">← Back to States</button>
            <h2 class="view-title">Districts in ${state}</h2>
            <div class="grid-container" id="districts-grid"></div>
        `;

        document.getElementById('back-to-states').addEventListener('click', renderStates);
        const grid = document.getElementById('districts-grid');

        const districts = schoolsData[state];
        Object.keys(districts).sort().forEach(district => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `<h3>${district}</h3>`;
            card.addEventListener('click', () => renderSchools(state, district));
            grid.appendChild(card);
        });
    }

    function renderSchools(state, district) {
        app.innerHTML = `
            <button class="back-btn" id="back-to-districts">← Back to Districts</button>
            <h2 class="view-title">Schools in ${district}, ${state}</h2>
            <div id="schools-list"></div>
        `;

        document.getElementById('back-to-districts').addEventListener('click', () => renderDistricts(state));
        const list = document.getElementById('schools-list');

        const schools = schoolsData[state][district];

        if (schools.length === 0) {
            list.innerHTML = '<p>No schools found in this district.</p>';
            return;
        }

        schools.forEach(school => {
            const card = document.createElement('div');
            card.className = 'school-card';

            const streamsHtml = school.streams.map(s => `<span class="tag">${s}</span>`).join('');

            card.innerHTML = `
                <h2>${school.name}</h2>
                <p><span class="label">Address:</span> ${school.address}</p>
                <p><span class="label">Level:</span> ${school.level}</p>
                <p><span class="label">Streams:</span> ${streamsHtml}</p>
                <p><span class="label">Phone:</span> ${school.phone || 'N/A'}</p>
                <p><span class="label">Email:</span> <a href="mailto:${school.email}" class="email-link">${school.email}</a></p>
            `;
            list.appendChild(card);
        });
    }

    function renderTrusts() {
        app.innerHTML = `
            <h2 class="view-title">Education Trusts & EdTech Companies</h2>
            <div id="trusts-list"></div>
        `;
        const list = document.getElementById('trusts-list');

        trustsData.forEach(item => {
            const card = document.createElement('div');
            card.className = 'school-card';
            card.innerHTML = `
                <h2>${item.name}</h2>
                <p><span class="label">Type:</span> ${item.type}</p>
                <p><span class="label">Address:</span> ${item.address}</p>
                <p><span class="label">Email:</span> <a href="mailto:${item.email}" class="email-link">${item.email}</a></p>
            `;
            list.appendChild(card);
        });
    }

    // Initialize
    loadData();
});
