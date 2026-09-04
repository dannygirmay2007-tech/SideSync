# SideSync

SideSync is a Flask web application I built to create fair teams for pickup soccer. Choosing teams by hand can be inconsistent, especially when every player brings different strengths, so I wanted to turn that real problem into a practical software project.

Instead of relying on a single overall rating, SideSync compares players across football IQ, technical ability, and athleticism to find the most balanced matchup available. Building it gave me the chance to work with backend development, databases, CRUD operations, and a custom scoring algorithm in one complete application.

## Technologies

- Python
- Flask
- SQLAlchemy
- SQLite
- Jinja
- HTML and CSS

## Core Features

- Add, edit, and delete players
- Store player ratings in SQLite
- Rate players from 1–10 in three soccer-specific categories
- Select the players participating in a session
- Generate and compare every unique equal-team split
- Automatically return the matchup with the lowest balance penalty

## Balancing Algorithm

For every valid equal-team split, SideSync calculates each team's average rating in three categories and measures the absolute difference between the teams. Those differences are combined into a weighted balance penalty:

```text
balance penalty =
    (Football IQ difference × 0.45)
  + (Technical Ability difference × 0.35)
  + (Athleticism difference × 0.20)
```

The split with the lowest penalty is selected. Football IQ receives the greatest weight because awareness, positioning, and decision-making affect both attack and defense. Technical ability remains a major factor in possession and execution, while athleticism is weighted lower so pace or strength alone does not dominate the result.

The categories are compared separately instead of collapsing every player into one overall score. This preserves distinct player profiles: two players can have similar overall ability while contributing in very different ways. SideSync therefore balances the composition of each team, not just its total talent.

## Setup and Run

1. Clone the repository and enter the project directory:

   ```bash
   git clone <repository-url>
   cd SideSync
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   On Windows:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   On macOS or Linux:

   ```bash
   source .venv/bin/activate
   ```

3. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   python app.py
   ```

5. Open the local address shown in the terminal.

## Usage

1. Add each player and assign ratings for Football IQ, Technical Ability, and Athleticism.
2. Select the players participating in the current game.
3. Choose **Generate Teams**.
4. Review the two teams and their balance score; a lower score represents a closer matchup.

SideSync requires an even number of selected players so both teams have the same size.

## Project Status

**V1 is complete.** The full player-management and team-balancing workflow is working, from saving player ratings to generating the best available team split. I am happy with the foundation and plan to use what I learned here in future projects and possible SideSync updates.

## Future Improvements

- Add automated tests for the scoring and team-generation logic
- Improve validation and user-facing error messages
- Warn when the best available split is still significantly uneven
- Add optional randomization between similarly balanced matchups
- Deploy the application for public use
- Explore an API-driven frontend and PostgreSQL for a future version
