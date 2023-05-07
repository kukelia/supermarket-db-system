# 🛒 Supermarket Database System Design and Application
Desing and implementation of a Normalized database in PostgreSQL🐘, and a Python🐍 application interface with it.
The project is fully dockerized🐳 and includes a "setup.sh" script file, which executes
the docker compose commands required for its functionality


### 🏆 Main challenges overcomed:

* Designing Database from scratch (ERD and implementation)
* Grouping App interface's operations in Transactions, and committing them when all requirements were satisfied
* Fully dockerizing the app, making it <strong>portable</strong> and <strong>scalable</strong>
  
### Physical data model:

<img src="https://github.com/kukelia/supermarket-db-system/blob/master/img/ERD.png" alt="drawing" width="1100"/>
Made with PGadmin4's ERD tool

### App connection code:

<img src="https://github.com/kukelia/supermarket-db-system/blob/master/img/app_connection.png" alt="drawing" width="900"/>

### SQL Query example:

<img src="https://github.com/kukelia/supermarket-db-system/blob/master/img/query_example.png" alt="drawing" width="900"/>
