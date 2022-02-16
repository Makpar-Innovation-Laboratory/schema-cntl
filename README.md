

Notes

1. there is no way to know, given two version of a schema with different fields, whether or not the fields were renamed or dropped/added. 

2. need to take the opinion that fields cannot be renamed once named. that way, the schema_cntl can determine what to do when it encounters new fields. 

3. data types of columns can still be altered, just not the name.
