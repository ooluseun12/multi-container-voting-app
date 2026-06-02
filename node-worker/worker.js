const { Client } = require("pg");

const client = new Client({
    host: "db",
    user: "postgres",
    password: "postgres",
    database: "foodvotes",
    port: 5432
});

async function monitorVotes() {

    await client.connect();

    console.log("Worker started...");

    setInterval(async () => {

        const result = await client.query(`
            SELECT food_option,
            COUNT(*) as votes
            FROM votes
            GROUP BY food_option
        `);

        console.clear();

        console.log("===== Vote Statistics =====");

        result.rows.forEach(row => {
            console.log(
                `${row.food_option}: ${row.votes}`
            );
        });

    }, 5000);
}

monitorVotes();
