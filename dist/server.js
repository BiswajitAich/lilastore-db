import express from "express";
import fs from "fs";
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const app = express();
app.get('/api', (req, res) => {
    const fetchData = req.query.fetchData;
    if (!fetchData) {
        return res.status(400).json({ err: "Parameter missing" });
    }
    const filePath = path.join(__dirname, '..', fetchData);
    console.log("Attempting to read file at:", filePath);
    fs.readFile(filePath, 'utf8', function (err, data) {
        if (err) {
            return res.status(500).json({ error: "Error reading file" });
        }
        console.log(data);
        res.end(data);
    });
});
let server = app.listen(8080, function () {
    const address = server.address();
    if (typeof address === 'string') {
        console.log("Pipe address: " + address);
    }
    else if (address && typeof address === 'object') {
        const host = address.address;
        const port = address.port;
        console.log("host: " + host + "\n" + "port: " + port);
    }
});
