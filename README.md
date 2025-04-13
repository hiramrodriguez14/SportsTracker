# PHASE 2:

# https://db-spring2025-phga-team-72c9b1d19c25.herokuapp.com/




# Troubleshooting

For logs:

heroku logs --tail --app db-spring2025-phga-team


IF WE DESTROY THE DATABASE

Add this to procfile and redeploy

release: python bug_handling/initial_db_creation.py && python ETL/call_all_etls.py

# --------------------------------------------------

# PHASE 1:

# heroku info

db url:
postgres://u5ie5npmv1rgvf:p5167c9c6edb4adfcd313ff0d0b54c4cc526b38ab65f3fdf9e9b704a6fe397473@cd1goc44htrmfn.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dfqftn892u378j

para datagrip:

Host: cd1goc44htrmfn.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com

Port: 5432

Authentication: User & Password

User: u5ie5npmv1rgvf

Password: p5167c9c6edb4adfcd313ff0d0b54c4cc526b38ab65f3fdf9e9b704a6fe397473

Database: dfqftn892u378j

SSL Mode: Require
