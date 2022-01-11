# Simpals Python coding task

## Running the app

1. Copy `.env.example` to `.env` and add your secret API key
2. Install [Docker](https://www.docker.com/get-started)  
3. Run `docker-compose up -d`  
4. Open http://localhost:8888/ in your web browser

**Note:** to see your changes in the code, run `docker restart simpals_app`


## Other Notes  

 - Thankfully user Johny194 has only 13 ads, so it is possible to fetch them all 
in one request. Otherwise, a proper pagination is required.
 - Very unfortunately, didn't have enough time to complete points 4 and 5. 
 - For point 4, I intended to add hash to each ad and regularly re-fetch all ads 
and compare their hashes with the ones in the database. For scheduler, 
I would set up cron task in the app container. 
