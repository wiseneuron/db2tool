Introduction

db2tool is a script help you to generate sql for db2. include,

 a) generate sql to export table data.
 
 b) generate sql to import table data.
 
 c) generate ddl of schema.

Dependencies

1.pydb2

http://sourceforge.net/projects/pydb2/

2.python 2.4+

Usage

read script db2tool.py

uncomment the line during 94~109line you want to execute.
     
exg, if you want to generate a sql for export a table , uncomment line 97
     
```python
print db2tool.gen_export_table_sql('table_to_export_data')
```
then, execute the command in console,
```bash     
python db2tool.py <dbname> <user_id> <password>
```
thus, you can get the sql or the ddl you want. read the comment in ``db2tool.py``.

author: neuron

if you want contact the author, please

visit http://idocbox.com/ or send mail to wiseneuron@gmail.com


thanks! Good luck!

