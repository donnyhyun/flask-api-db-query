CREATE DATABASE authentication;
CREATE DATABASE catalog;
CREATE DATABASE quest;

USE authentication;

CREATE TABLE Users (
    user_id INT NOT NULL,
    user_name VARCHAR(255),
    gold INT DEFAULT 0,
    diamond INT DEFAULT 0,
    status ENUM('new', 'not_new', 'banned') DEFAULT 'new',
    PRIMARY KEY (user_id),
);

USE catalog;

CREATE TABLE Rewards (
    reward_id INT NOT NULL,
    reward_name VARCHAR(255),
    reward_item VARCHAR(255),
    reward_qty INT,
    PRIMARY KEY (reward_id)
);

CREATE TABLE Quests (
    quest_id INT NOT NULL,
    reward_id INT NOT NULL,
    auto_claim BOOLEAN DEFAULT false,
    streak INT,
    duplication INT,
    name VARCHAR(255),
    description VARCHAR(255),
    PRIMARY KEY (quest_id),
    FOREIGN KEY (reward_id) REFERENCES Rewards(reward_id)
);

USE quest;

CREATE TABLE user_quest_rewards (
    user_id INT NOT NULL,
    quest_id INT NOT NULL,
    status ENUM('claimed', 'not_claimed') DEFAULT 'not_claimed',
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    curr_streak INT NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES authentication.Users(user_id),
    FOREIGN KEY (quest_id) REFERENCES catalog.Quests(quest_id)
);


INSERT INTO catalog.Rewards
    (reward_id, reward_name, reward_item, reward_qty)
VALUES
    (1, 'Ten Diamonds', 'diamond', 10)

INSERT INTO catalog.Quests
    (quest_id, reward_id, auto_claim, streak, duplication, name)
VALUES
    (1, 1, false, 3, 2, "sign-in-three-times")