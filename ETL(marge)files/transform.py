import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    df['last_updated'] = pd.to_datetime(df['last_updated'])
    datetime_dim = df[['last_updated']].drop_duplicates().reset_index(drop=True)
    datetime_dim['update_hour'] = datetime_dim['last_updated'].dt.hour
    datetime_dim['update_day'] = datetime_dim['last_updated'].dt.day
    datetime_dim['update_month'] = datetime_dim['last_updated'].dt.month
    datetime_dim['update_year'] = datetime_dim['last_updated'].dt.year
    datetime_dim['update_weekday'] = datetime_dim['last_updated'].dt.weekday
    datetime_dim['datetime_id'] = datetime_dim.index+1
    airport_coordinates_dim = df[['latitude_deg','longitude_deg','elevation_ft']].drop_duplicates().reset_index(drop=True)
    airport_coordinates_dim['coordinates_id'] = airport_coordinates_dim.index+1
    airport_coordinates_dim['elevation_ft'] = airport_coordinates_dim['elevation_ft'].fillna(0)
    regions_dim = df[['region_name','local_region']].drop_duplicates().reset_index(drop=True)
    regions_dim['region_id'] = regions_dim.index+1
    cities_dim = df.merge(regions_dim,on=['region_name','local_region'])[['municipality','region_id']].drop_duplicates().reset_index(drop=True)
    cities_dim['city_id']  =cities_dim.index+1
    airport_type_dim = df[['type']].drop_duplicates().reset_index(drop=True)
    airport_type_dim['type_id'] = airport_type_dim.index+1
    fact_table = df.merge(datetime_dim, on='last_updated').merge(airport_coordinates_dim,on=['latitude_deg','longitude_deg']).merge(cities_dim,on='municipality').merge(airport_type_dim,on='type')[['name','ident','scheduled_service','score','type_id','city_id','coordinates_id','datetime_id']]
    
    return {"datetime_dim":datetime_dim.to_dict(orient="dict"),
    "airport_coordinates_dim":airport_coordinates_dim.to_dict(orient="dict"),
    "regions_dim":regions_dim.to_dict(orient="dict"),
    "cities_dim":cities_dim.to_dict(orient="dict"),
    "airport_type_dim":airport_type_dim.to_dict(orient="dict"),
    "fact_table":fact_table.to_dict(orient="dict")}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
