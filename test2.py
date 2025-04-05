from controller.dataset_controller import DatasetController as dc
from datetime import date

df=dc.get_default_dataset()
print(len(df))
the_date=date(2025,5,2)
new_df=dc.search_after(df,the_date)
print(len(new_df))
new_df=dc.search_before(df,the_date)
print(len(new_df))

new_df=dc.search_less_than(df,100)
print(len(new_df))
new_df=dc.search_more_than(df,100)
print(len(new_df))
new_df=dc.search_between_amount(df,300,200)
print(len(new_df))
print(new_df)
search_term='user'
new_df=dc.search_by_term(df,search_term)
print(len(new_df))
