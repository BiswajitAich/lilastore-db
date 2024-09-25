const { spawn } = require("child_process");
const express =  require("express");
const app = express();

app.get('/recomendation',function(req: any, res: any){
    const id = req.query.id;
    if(!id) {
        return res.status(400).json({err: "Parameter missing" })
    }
    const childPython = spawn('python', ['recomendationSystem.py', id])
    let pythonData = '';
    childPython.stdout.on('data', (data: any) => {
        pythonData += data.toString();
    })
    childPython.stderr.on('data', (data: any) => {
        console.error('stderr:', data.toString());
        res.status(500).send("Python script error");    
    })
    childPython.on('close', (code: number) => {
        console.log(`Python script exited with code ${code}`);
        if (code === 0) {
            res.status(200).json(JSON.parse(pythonData)); 
        } else {
            res.status(500).send("Failed to get recommendations");
        }
    });
})

app.listen(3000, () => {
    console.log("Server is running on port 3000");
});