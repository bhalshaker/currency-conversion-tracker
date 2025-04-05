from controller.dataset_controller import DatasetController as dc
from datetime import date

df=dc.get_default_dataset()
print(len(df))
the_date=date(2025,5,2)
new_df=dc.search_after(df,the_date)
print(len(new_df))
new_df=dc.search_before(df,the_date)
print(len(new_df))