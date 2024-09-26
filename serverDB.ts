import express, { Request, Response } from 'express';
import { spawn } from "child_process";
const app = express();

app.get('/get-recommendation', (req: any, res: any) => {
    try {
        const id = req.query.id as string | undefined;
        if (!id) {
            return res.status(400).json({ err: "Parameter missing" })
        }
        const childPython = spawn('python', ['./recommendation/getRecommendation.py', id])
        let pythonData = '';
        let errorOccurred = false;
        childPython.stdout.on('data', (data: any) => {
            pythonData += data.toString();
        })
        childPython.stderr.on('data', (data: any) => {
            console.error('stderr:', data.toString());
            errorOccurred = true;
            res.status(500).send("Python script error");
        })
        childPython.on('close', (code: number) => {
            console.log(`Python script exited with code ${code}`);
            if (code === 0 && !errorOccurred) {
                res.status(200).json(JSON.parse(pythonData));
            } else if (!errorOccurred) {
                res.status(500).send("Failed to get recommendations");
            }
        });
    } catch (error) {
        console.error("Error:", error);
        res.status(500).send("Internal Server Error");
    }
})

app.get('/set-recommendation', (_req, res: Response) => {
    try {
        const childPython = spawn('python', ['./recommendation/recommendationSystem.py'])
        let errorOccurred = false;

        childPython.stderr.on('data', (data: any) => {
            console.error('stderr:', data.toString());
            errorOccurred = true;
        })

        childPython.on('close', (code: number) => {
            console.log(`Python script exited with code ${code}`);
            if (code === 0 && !errorOccurred) {
                res.status(200).json('successfully updated');
            } else if (!errorOccurred) {
                res.status(500).send("Failed to get recommendations");
            }
        });
    } catch (error) {
        console.error("Error:", error);
        res.status(500).send("Internal Server Error");
    }
})


app.use("/", (_req: Request, res: Response) => {
    res.json({ message: "backend api for private use" });
})
app.listen(7777, () => {
    console.log("Server is running on port 7777");
});