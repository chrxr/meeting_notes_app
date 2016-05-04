###To do

- [ ] Add in better validation on forms
- [ ] Add in new way to add attendees
    - This will be based on adding email addresses in gmail
    - When starts typing a name, it will auto-check against the database
- [ ] Need to isolate individual users' contacts and meetings, currently they are global
- [ ] Add in authentication model
- [ ] Change 'startTime' and 'endTime' in agenda model to 'length'
- [ ] Validate 'length' for all agenda points in meeting against total length of meeting
- [x] Create 'actions' model, with ParentalKey to notes (which in turn is owned by Action)
