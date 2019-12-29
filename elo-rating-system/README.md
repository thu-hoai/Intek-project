# Elo Rating System
---

## Description

- Purposes: for those who would like to build an Elo Rating System.

- Demonstrate the way to build Elo Rating Sys step by step: 
     - Waypoint 1: Class `Player`
     - Waypoint 2: Class `MatchResult`
     - Waypoint 4: Command-Line Interface Script
     - Waypoint 5: Command-Line Arguments Support
     - Waypoint 6: Expected Score Calculation
     - Waypoint 7: Match Outcome Player Score Calculation
     - Waypoint 8: Player Rating Update Calculation
     - Waypoint 9: Player Rating Update
     - Waypoint 10: Match Results Processing
     - Waypoint 11: Rating Update Calculation Improvement

- _Note_ : _more details, please refer to initial_istruction.md file_

## Method

_What is the Elo Rating System?_

The Elo Rating System (Elo) is a rating system used for rating players in games. 
Each player is assigned a number as a rating. The system predicts the outcome of a match between two players by using an expected score formula.

Everytime a game is played, the Elo rating of the participants change depending on the outcome and the expected outcome. The winner takes points from the loser; the amount is determined by the players' scores and ratings

- The classic Elo rating calculation: A win is counts as a score of 1, loss is a score of 0, and draw is a score of 0.5.
- The advanced calculation method: The score will be calculated as fomular: 
     ```
     score = player points/(player points + opponent points)
     ```

_Calculations_

If Player A has a rating of R<sub>A</sub> and Player B a rating of R<sub>B</sub>, the exact formula for Player A's score is:

![alt text](https://wikimedia.org/api/rest_v1/media/math/render/svg/51346e1c65f857c0025647173ae48ddac904adcb)

And Player B's score is:

![alt text](https://wikimedia.org/api/rest_v1/media/math/render/svg/4b340e7d15e61ee7d90f428dcf7f4b3c049d89ff)

Supposing Player A was expected to score E<sub>A</sub> points but actually scored S<sub>A</sub> points. The formula for updating his/her rating is:

![alt text](https://wikimedia.org/api/rest_v1/media/math/render/svg/09a11111b433582eccbb22c740486264549d1129)


---
## How to use

### Prerequisites
- Python3 installation is required to get started (check by using python3 --version)

### Usage
- Clone this repo to your local machine using `https://github.com/intek-training-jsc/elo-rating-system-alumni-2019-10-hoaithu1.git`
- Chmod +x elo.py
- Run as below:
    - In case using the classic Elo rating calculation (see method above)

     ```shell
     $ ./elo.py --p ~/whatever-csv-file
     ```
     - In case using advanced calculation method (see method above)
         
     ```shell
     $ ./elo.py -a --p ~/whatever-csv-file
     ```

## Support

Reach out to me (author)at the following place!

- Email at hoai.le@f4.intek.edu.vn
---
