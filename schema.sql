create table if not exists articles (
  id integer primary key autoincrement,
  author string not null,
  slug string not null,
  title string not null,
  body string not null,
  published datetime,
  updated datetime,
  created datetime default current_timestamp
);
