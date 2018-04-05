# determine os
unameOut="$(uname -s)"
case "${unameOut}" in
    Darwin*)    pg_cmd="psql -U postgres";;
    *)          pg_cmd="sudo -u postgres psql"
esac

${pg_cmd} -c "DROP DATABASE IF EXISTS geonames_sunil"
${pg_cmd} -c "DROP ROLE IF EXISTS geonames_user"
${pg_cmd} -c "CREATE USER geonames_user WITH PASSWORD 'password';"
# needed to create postgis extension
${pg_cmd} -c "ALTER ROLE geonames_user superuser;"
${pg_cmd} -c "CREATE DATABASE geonames_sunil ENCODING 'UTF8';"
${pg_cmd} -c "GRANT ALL PRIVILEGES ON DATABASE geonames_sunil TO geonames_user;"

cat sql/create_table.sql | ${pg_cmd} -d geonames_sunil -a
