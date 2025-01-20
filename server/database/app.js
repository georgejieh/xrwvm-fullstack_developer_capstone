const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

mongoose.connect("mongodb://mongo_db:27017/", { dbName: 'dealershipsDB' });

const Reviews = require('./review');
const Dealerships = require('./dealership');

try {
  Reviews.deleteMany({}).then(() => {
    Reviews.insertMany(reviews_data['reviews']);
  });
  Dealerships.deleteMany({}).then(() => {
    Dealerships.insertMany(dealerships_data['dealerships']);
  });
} catch (error) {
  console.error('Error seeding database:', error);
}

// Express route to home
app.get('/', async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews for dealer' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find(); // Retrieve all dealerships
    res.json(documents); // Return all dealerships
  } catch (error) {
    console.error('Error fetching dealerships:', error);
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Express route to fetch dealerships by state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const state = req.params.state; // Get the state from the URL
    const documents = await Dealerships.find({ state: state }); // Filter dealerships by state
    if (documents.length > 0) {
      res.json(documents); // Return dealerships for the state
    } else {
      res.status(404).json({ error: `No dealerships found in state: ${state}` });
    }
  } catch (error) {
    console.error('Error fetching dealerships by state:', error);
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

// Express route to fetch a dealer by ID
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const id = req.params.id; // Get the dealer ID from the URL
    const document = await Dealerships.findOne({ id: id }); // Find dealership by ID
    if (document) {
      res.json(document); // Return the dealership
    } else {
      res.status(404).json({ error: `Dealer with ID ${id} not found` });
    }
  } catch (error) {
    console.error('Error fetching dealer by ID:', error);
    res.status(500).json({ error: 'Error fetching dealer by ID' });
  }
});

// Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  const data = JSON.parse(req.body);
  const documents = await Reviews.find().sort({ id: -1 });
  const new_id = documents[0]['id'] + 1;

  const review = new Reviews({
    "id": new_id,
    "name": data['name'],
    "dealership": data['dealership'],
    "review": data['review'],
    "purchase": data['purchase'],
    "purchase_date": data['purchase_date'],
    "car_make": data['car_make'],
    "car_model": data['car_model'],
    "car_year": data['car_year'],
  });

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});