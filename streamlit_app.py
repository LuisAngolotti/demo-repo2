import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import sqlite3


def convert_table_to_df(db_path, table_name):
    dat = sqlite3.connect(db_path)
    query = dat.execute("""SELECT * FROM {}""".format(table_name))
    cols = [column[0] for column in query.description]
    results = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    return results


df = convert_table_to_df("track_metadata.db", "songs")

# display(df)


def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection


# iris = pd.read_csv(
#    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
# )

selection = aggrid_interactive_table(df=df)

if selection:
    st.write("You selected:")
    st.json(selection["selected_rows"])
