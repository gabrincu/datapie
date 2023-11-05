# Roadmap for Datapie

## 0.1 version

First version to consider making a release must have these features:

- [x] Configurable adapters to MySQL, Psql and SQLite
- [x] Storable config in a "$XDG_CONFIG_HOME/datapie/datapie.toml" file
- [x] Run query -> catch errors -> see results in Table View
- [ ] Limit queries naturally and add pagination to Table View so that we don't get a stuck app.
- [x] App is refactored with Textual good practices (Messages, Reactive attributes for Widgets, different Screens)
- [ ] Enable adding more connections in a modal window without editing the file manually
- [ ] Write some basic tests


## 0.1.1 version

- [ ] Add Github workflows
- [x] Export to CSV entire Table View
- [x] Select entire rows using V in Table View
- [ ] Export to CSV only selected rows from Table View

## 0.1.2 version

- [ ] Create a "Command Mode" for the Table View that enables selections and edits using vim-like regex and persists any changes to DB
