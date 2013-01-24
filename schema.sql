create table if not exists articles (
  id integer primary key autoincrement,
  slug string not null,
  title string not null,
  body string not null,
  published date default current_date
);
