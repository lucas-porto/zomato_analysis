
#Libraries
import pandas as pd

# Helper Functions
def load_data(file_path, file_path_2):
  """
  Loading ours dataframe.
  """

  df1 = pd.read_csv(file_path, encoding='latin-1')
  df2 = pd.read_csv(file_path_2, encoding='latin-1')

  return df1, df2

def rename_columns(x):
  """
  Renaming columns names of dataframe transforming in a snakecase.
  """

  x = x.replace(' ', '_')
  x = x.lower()
  return x

def merging_data(df1, df2, key_df1, key_df2):
  """
  Merging dataframes.
  """

  df_out = pd.merge(df1, df2, on=[key_df1,key_df2])
  return df_out

def create_price_type(price_range):
  """
  Creating a group for our price range.
  """

  if price_range == 1:
      return "cheap"
  elif price_range == 2:
      return "normal"
  elif price_range == 3:
      return "expensive"
  else:
      return "gourmet"

def drop_constant_columns(dataframe):
  """
  Drops constant value columns of dataframe.
  """

  keep_columns = dataframe.columns[dataframe.nunique()>1]
  return dataframe.loc[:,keep_columns].copy()

COLORS = {
    "Dark Green": "darkgreen",
    "Green": "green",
    "Yellow": "lightgreen",
    "Orange": "orange",
    "Red": "red",
    "White": "lightgray",
}

def color_name(color_code):
    return COLORS[color_code]

def preparing_data(file_path, file_path_2):
  """
  Preparing dataframe with pre-selected adjusts.
  """
  data_origin, data_side_origin = load_data(file_path, file_path_2)

  data = data_origin.copy()
  data_side = data_side_origin.copy()

  # adjusting columns names
  data.columns = data.rename(columns=rename_columns).columns
  data_side.columns = data_side.rename(columns=rename_columns).columns

  #inserting country names
  data = merging_data(data, data_side, 'country_code', 'country_code')

  # droping columns
  drop_columns = ['locality_verbose','country_code']
  data = data.drop(columns=drop_columns)

  #removing nulls
  data  = data[~data.cuisines.isnull()]

  # correcting names with wrong spelling
  dict_to_correct = {'Sao Paulo' : ['Sí£o Paulo'],
                   'Brasilia' : ['Brasí_lia'] ,
                    'Instabul' : ['ÛÁstanbul']
                    }

  dict_map = {v: k for k, v in dict_to_correct.items() for v in v}
  data['city'] = data['city'].replace(dict_map) 
  
  #creating a new column
  data["price_type"] = data.loc[:, "price_range"].apply(lambda x: create_price_type(x))

  #adjust the cusine types and selecting the first description.
  data["cuisines"] = data.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

  #creating colors for folium
  data["color_name"] = data.loc[:, "rating_color"].apply(lambda x: color_name(x))

  data = drop_constant_columns(data)

  data.to_csv('./data/processed/zomato.csv', index=False)
  
  return data




