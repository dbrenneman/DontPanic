create table if not exists articles (
  id integer primary key autoincrement,
  slug text not null,
  title text not null,
  body text not null,
  updated timestamp not null,
  published timestamp not null
);
