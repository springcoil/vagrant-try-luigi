# Create a vagrant database user ...
# TODO: may fail but will work the first time. Dirty and nasty. FIXME
createuser -D -l -R -S vagrant || /bin/true:
  cmd.run:
    - user: postgres

# ... and a vagrantdb database
createdb -O vagrant vagrantdb || /bin/true:
  cmd.run:
    - user: postgres

psql vagrantdb --command "ALTER USER vagrant WITH PASSWORD 'vagrant';":
  cmd.run:
    - user: postgres
