DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS analysis_page;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE analysis_page (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  file_dir TEXT NOT NULL,
  yaml_file_dir TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);
