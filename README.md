# SideSync

SideSync is a pickup soccer team-balancing web app that creates fair teams based on player ratings.

## Features

- Add, edit, and delete players
- Store player ratings with SQLite
- Select which players are playing
- Generate every valid equal-team split
- Compare teams using weighted player categories
- Automatically choose the most balanced matchup
- Display the generated teams in a styled results page

## Tech Stack

- Python
- Flask
- SQLAlchemy
- SQLite
- HTML
- CSS

## How the Balancing Algorithm Works

Each player is rated in three categories:

- **Football IQ** — decision-making, positioning, awareness, movement, and defensive intelligence
- **Technical Ability** — passing, first touch, dribbling, ball control, shooting, and execution
- **Athleticism** — pace, agility, stamina, strength, and physical ability

The categories are weighted based on how much they affect pickup soccer:

- Football IQ: **45%**
- Technical Ability: **35%**
- Athleticism: **20%**

For every possible equal-team split, SideSync:

1. Calculates each team’s average rating in all three categories
2. Finds the difference between the two teams in each category
3. Applies the category weights
4. Adds those differences into one balance penalty

```text
balance penalty =
    (IQ difference × 0.45)
  + (Technical difference × 0.35)
  + (Athleticism difference × 0.20)
```

The matchup with the lowest balance penalty is selected.

### Design Decisions

SideSync compares categories separately instead of giving each player one overall rating.

This preserves different player profiles. A player with high Football IQ but average Technical Ability should not be treated exactly the same as a highly technical player with lower awareness, even if their overall ability seems similar.

The algorithm also removes mirrored duplicate matchups so that each unique team split is only evaluated once.

A low balance score means the selected teams are closely matched. A high score can indicate that the player pool itself cannot be divided into truly even teams.

## Why I Built It

My friends and I regularly play pickup soccer, and creating fair teams can be difficult when players have different strengths.

I built SideSync to solve that problem while learning backend development, databases, web applications, and algorithm design.

## What I Learned

Through SideSync, I practiced:

- Flask routing and HTTP GET/POST requests
- CRUD operations
- Form handling and validation
- SQLAlchemy and relational database concepts
- Jinja templates
- Python combinations and list comprehensions
- Designing and testing a custom scoring algorithm
- Git and GitHub workflow
- Refactoring application logic into cleaner functions

## Running Locally

1. Clone the repository:

```bash
git clone <your-repository-url>
```

2. Create and activate a virtual environment.

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
python app.py
```

5. Open the local Flask address shown in the terminal.

## Future Improvements

- Deploy the application
- Add a warning when the best available matchup is still noticeably uneven
- Improve validation and error handling
- Add automated tests
- Explore a REST API and more interactive frontend