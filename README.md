# pairing

Randomly match people for pair programming.

## Minimum Requirements

* [Python 3.11+](https://www.python.org/downloads/)

## Usage

* Fill out `people.csv` with the first names of the people you want to pair, followed by skill level, and today's date.
    ```
    name,skill_level,date
    pythoninthegrass,3,2024-05-18
    ```
* Levels are as follows:

| Level | Description       |
| ----- | ----------------- |
| 0     | Novice            |
| 1     | Advanced beginner |
| 2     | Competent         |
| 3     | Proficient        |
| 4     | Expert            |

* Once the csv is filled out, run the script:
    ```bash
    python pairing.py
    ```

## Exclusions

If you want to exclude certain people from pairing with each other, add them to the `exclusions.csv` file. The format is as follows:

```
person1,person2
```
