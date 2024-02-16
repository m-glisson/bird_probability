const express = require('express');
const { engine } = require('express-handlebars');

const fs = require('fs');

const Papa = require('papaparse');

const app = express();
app.use(express.static('public'));
app.engine('handlebars', engine());
app.set('view engine', 'handlebars');
app.set('views', './views');



app.get('/', (req, res) => {
    //Serves the body of the page aka "main.handlebars" to the container //aka "index.handlebars"
    res.render('main', {layout : 'index'});
    });

app.get('/health', (req, res) => {
    res.send('Hello World!')
});

app.get('/api/data', (req, res) => {
    const data = [100, 50, 300, 40, 350, 250]; // assuming this is coming from the database
    res.json(data);
});

app.get('/api/markov-chain', (req, res) => {
    // read the file ../data/miserable.json then return the parsed json object
    const file = fs.readFileSync('../data/all-markov-chain-states.json', 'utf8');
    const data = JSON.parse(file);
    res.json(data);
});

app.listen(8081);