import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';

const app = express(); 
const PORT = 2408;

app.use(cors());
app.use(express.json());

// Mapping of symbols to CoinGecko's coin ID
const cryptoMapping = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "BNB": "binancecoin",
    "SOL": "solana",
    "XRP": "ripple",
    "ADA": "cardano"
};

app.get('/api/crypto/:symbol', async (req, res) => {
    const symbol = req.params.symbol.toUpperCase();
    console.log("Requested Crypto:", symbol);

    if (!cryptoMapping[symbol]) {
        return res.status(400).json({ error: "Invalid crypto symbol" });
    }

    try {
        const response = await fetch(`https://api.coingecko.com/api/v3/coins/${cryptoMapping[symbol]}/market_chart?vs_currency=usd&days=7`);
        const data = await response.json();

        if (!data || !data.prices) {
            return res.status(500).json({ error: "Invalid response from API" });
        }

        const chartData = data.prices.map(([timestamp, price]) => ({
            time: new Date(timestamp).toLocaleDateString(),
            price: price
        }));

        res.json(chartData);
    } catch (error) {
        console.error("Error fetching crypto data:", error);
        res.status(500).json({ error: "Failed to fetch crypto data" });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
