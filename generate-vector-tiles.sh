tippecanoe -e data/borders_tiles \
    --drop-densest-as-needed --extend-zooms-if-still-dropping \
    -Z0 -z10 \
    --no-tile-compression \
    -l borders \
    --allow-existing data/borders_geojsons/*.geojson
