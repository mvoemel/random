# Agreement on code of conduct

## Regular meetings and exchanges

Good communication within the team is an important prerequisite that has a major impact on the success of the project.
Regular meetings and a continuous exchange are required to discuss challenges and decisions within the team and to
monitor the progress of the project. All team members should meet at least twice a week in a longer meeting to discuss
the current status. A communication channel (WhatsApp, Teams, ...) is created for continuous exchange between meetings
and "emergencies", through which both time-critical and smaller matters can be discussed.

## Collaborative working environment

Version control systems such as Git make it easy to implement and manage software projects in a team. In this software
project, the aim is now to use more advanced workflows and actions from Git to minimize difficulties and problems when
working on the project. Services such as collaborative coding ("Code with Me" from Jetbrain's IDE) are also to be
tested, as they offer a promising way of working in a team. These services are comparable to Google Docs, where several
members have access to a member's code. Team members who are unable to attend a meeting in person can also help others
solve coding challenges more easily.

## Defined distribution of roles

As different areas and services are covered in PM2, it makes sense to define and distribute the roles in the team. We
will assign main roles such as team leader, minute taker, etc. When implementing the project (programming part), we will
also assign "secondary roles". These are distributed according to the planning of the program (class diagram, etc.) and
are intended to determine in which "rough" area a team member will make a contribution. These areas include program
classes, testing concepts, graphical user interface (GUI design) and other components of software development.

## Commit agreement

| Keyword  | Explanation                              |
|----------|------------------------------------------|
| FEAT     | new feature or change to a feature       |
| FIX      | fix a bug                                |
| FORMAT   | code formatting, code comments           |
| DOCS     | changes to the documentation             |
| TEST     | add test cases or change tests           |
| MAINT    | maintenance files such as workflow files |
| REFACTOR | code refactor                            |

### Examples

```
FEAT(logger): Support .txt Files
```

```
FIX: Avoid deadlocks when using multiple Players
```

```
TEST(driving): Increased test coverage of driving function
```

```
REFACTOR(users): Removed old Car.java Implementation

Because of this and that, the Car Model was redesigned according to that.

Implements #69
```

```
MAINT: added en_UK.json
```

## Branches agreement

If a member wants to work on a feature, bug fix, etc., they must perform the following steps:

1) **Create and/or assign an issue**: Create and/or assign an issue to yourself and put it in the *In progress* lane one
   the board.
1) **Create new branch**: Create new branch on the issue page from branch `dev` (e.g. `32-your-issue-title`).
2) **Changes committed**: Commit changes to the `32-your-issue-title` branch with the above-mentioned commit agreement.
3) **Create pull request**: When the change is completed, create a pull request.
4) **Review Pull Request**: Pull Request must be reviewed by at least two other members.
5) **Merge Pull Request**: After the pull request has been reviewed and approved, it can be merged into the `dev`
   branch.

In case of a release, the `dev` branch is merged into `main`.

## Issue types

- feature
- bug
- refactor
- task
- documentation
- test

## Board agreement

Following lanes are used in the Kanban board:

- **Backlog**: This lane represents tasks or issues that have been identified for future implementation but have not yet
  been scheduled for execution. It serves as a repository for ideas and requirements awaiting prioritization.
- **Ready**: Issues in this lane are prepared and prioritized for implementation. They have been analyzed, scoped, and
  are ready to be picked up by team members for execution.
- **In progress**: Tasks in this lane are currently being worked on by team members. Work-in-progress (WIP) limits are
  often applied to this lane to ensure that the team doesn't take on too much work simultaneously, thereby optimizing
  flow and productivity.
- **Postponed**: Issues in this lane were previously deemed important but have been deferred for various reasons, such
  as dependency issues, resource constraints, or changing priorities. They remain visible on the board for future
  consideration.
- **In Review**: Tasks that have been completed but require validation, testing, or feedback before being considered
  fully done are placed in this lane. They await approvals from other team members.
- **Done**: This lane signifies tasks that have been successfully completed and delivered. After a period of time the
  issues can be archived.

## Logger agreement

The following table shows the logging levels and the value corresponding to it:

| Level                   | Value             | Used for                          |
|-------------------------|-------------------|-----------------------------------|
| FINEST                  | 300               | Specialized Developer Information |
| FINER                   | 400               | Detailed Developer Information    |
| FINE                    | 500               | General Developer Information     |
| CONFIG                  | 700               | Configuration Information         |
| INFO                    | 800               | General Information               |
| WARNING                 | 900               | Potential Problem                 |
| SEVERE                  | 1000              | Represents serious failure        |
| OFF (Special Log Level) | Integer.MAX_VALUE | Turns off the logging             |
| ALL (Special Log Level) | Integer.MIN_VALUE | Captures everything               |

Examples:

```
Logger.getLogger(Database.class.getName()).log(Level.SEVERE, "Error connecting to database: " + e.getMessage());
```

```
// Defined at the top of the class
Logger logger = Logger.getLogger(ViewFactory.class.getName());

logger.log(Level.SEVERE, "Error creating new Scene: " + e.getMessage())
```
