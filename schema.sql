drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  slug string not null,
  title string not null,
  text string not null,
  posted date
);
