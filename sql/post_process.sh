# determine os
unameOut="$(uname -s)"
case "${unameOut}" in
    Darwin*)    pg_cmd="psql -U postgres";;
    *)          pg_cmd="sudo -u postgres psql"
esac

cat sql/create_geom_column.sql | ${pg_cmd} -d geonames_sunil -a
cat sql/create_indices.sql | ${pg_cmd} -d geonames_sunil -a