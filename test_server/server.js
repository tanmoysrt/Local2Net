require('dotenv').config();

const PORT=3000;

// Express
const express = require('express');
// HTTP Logger
const morgan = require('morgan');
// Cors
const cors = require('cors');

const app = express();
// app.use(helmet());
app.disable('x-powered-by')
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cors({
    origin: '*',
    optionsSuccessStatus: 200
}))

app.use(morgan('dev'));


app.get('/', (req, res) => {
    res.send({
        message: 'Hello World',
        method: "GET"
    });
})

app.post('/', (req, res) => {
    res.send({
        message: 'Hello World',
        method: "POST"
    });
})

app.patch('/', (req, res) => {
    res.send({
        message: 'Hello World',
        method: "PATCH"
    });
})

app.put('/', (req, res) => {
    res.send({
        message: 'Hello World',
        method: "PUT"
    });
})

app.delete('/', (req, res) => {
    res.send({
        message: 'Hello World',
        method: "DELETE"
    });
})

app.options('/', (req, res) => {
    res.send({
        message: 'Hello World',
        method: "OPTIONS"
    });
})

app.listen(PORT, () => console.log(`🚀 @ http://localhost:${PORT}`));
