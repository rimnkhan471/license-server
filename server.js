const express = require('express');
const fs = require('fs');
const app = express();
const PORT = process.env.PORT || 3000;

let licenses = require('./licenses.json');

app.get('/validate', (req, res) => {
    const key = req.query.key;
    if (!key) return res.send("INVALID");

    const license = licenses.licenses.find(l => l.license_key === key);
    if (!license) return res.send("INVALID");

    const now = new Date();
    const expire = new Date(license.expire);

    if (license.blocked || license.used >= license.max_devices || now > expire) {
        return res.send("INVALID");
    }

    // Update used count
    license.used += 1;
    fs.writeFileSync('./licenses.json', JSON.stringify(licenses, null, 2));

    return res.send("VALID");
});

app.listen(PORT, () => {
    console.log(`License API running on port ${PORT}`);
});