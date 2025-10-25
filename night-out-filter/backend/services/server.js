
const pool = new Pool({
  connectionString: 'postgresql://username:password@localhost:5432/mydb'
});

// fetch all cards with optional query filtering
app.get('/cards', async (req, res) => {
  try {
    const { mood, budget, type } = req.query;
    const { rows: cards } = await pool.query('SELECT * FROM cards');
    
    const filtered = cards.filter(card => {
      if (mood && !card.tags.includes(mood)) return false;
      if (budget && card.price !== budget) return false;
      if (type && !card.tags.includes(type)) return false;
      return true;
    });

    res.json(filtered);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch cards' });
  }
});

// like a card
app.post('/like', async (req, res) => {
  try {
    const { user_name, card_id } = req.body;

    // get or create user
    let user = await pool.query('SELECT * FROM users WHERE name = $1', [user_name]);
    if (user.rows.length === 0) {
      const insertUser = await pool.query(
        'INSERT INTO users(name) VALUES($1) RETURNING *',
        [user_name]
      );
      user = insertUser;
    }

    const user_id = user.rows[0].user_id;

    // insert liked card
    await pool.query(
      'INSERT INTO liked_cards(user_id, card_id) VALUES($1, $2) ON CONFLICT DO NOTHING',
      [user_id, card_id]
    );

    res.json({ success: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to like card' });
  }
});

// get top 5 recommendations
app.get('/recommend/:user_name', async (req, res) => {
  try {
    const user_name = req.params.user_name;
    const { rows: userRows } = await pool.query('SELECT * FROM users WHERE name=$1', [user_name]);
    if (userRows.length === 0) return res.json([]);

    const user_id = userRows[0].user_id;

    // Get liked cards
    const { rows: likedRows } = await pool.query(
      'SELECT card_id FROM liked_cards WHERE user_id=$1',
      [user_id]
    );
    const likedCardIds = likedRows.map(r => r.card_id);

    if (likedCardIds.length === 0) return res.json([]);

    // Get tags of liked cards
    const { rows: likedCards } = await pool.query(
      'SELECT tags FROM cards WHERE id = ANY($1)',
      [likedCardIds]
    );

    // build tag frequency map
    const tagMap = {};
    likedCards.forEach(card => {
      card.tags.forEach(tag => {
        tagMap[tag] = (tagMap[tag] || 0) + 1;
      });
    });

    // Score all cards
    const { rows: allCards } = await pool.query('SELECT * FROM cards');
    const scoredCards = allCards
      .filter(card => !likedCardIds.includes(card.id))
      .map(card => {
        let score = card.tags.reduce((sum, tag) => sum + (tagMap[tag] || 0), 0);
        return { ...card, score };
      });

    // top 5
    scoredCards.sort((a, b) => b.score - a.score);
    const top5 = scoredCards.slice(0, 5);

    res.json(top5);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to generate recommendations' });
  }
});

app.listen(3000, () => console.log('Server running on port 3000'));
