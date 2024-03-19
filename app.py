import plotly.express as px
import seaborn as sns
import palmerpenguins
from shiny import render
from shiny import reactive, render, req
from shiny.express import input, ui
from shinywidgets import render_plotly
from shinywidgets import render_widget
import shinyswatch
from shiny import reactive
import pandas as pd

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

#Setting Theme
shinyswatch.theme.superhero()

#Title
ui.page_opts(title="Vetter M2 Penguins", fillable=True)

# Add a Shiny UI sidebar for user interaction
# Use the ui.sidebar() function to create a sidebar
# Set the open parameter to "open" to make the sidebar open by default
# Use a with block to add content to the sidebar
# Use the ui.h2() function to add a 2nd level header to the sidebar
#   pass in a string argument (in quotes) to set the header text to "Sidebar"
with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.hr()
    
# Use ui.input_selectize() to create a dropdown input to choose a column
#   pass in three arguments:
#   the name of the input (in quotes), e.g., "selected_attribute"
#   the label for the input (in quotes)
#   a list of options for the input (in square brackets) 
#   e.g. ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    
    ui.input_selectize("selected_attribute", "Attribute Selected", 
                       ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

# Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
#   pass in two arguments:
#   the name of the input (in quotes), e.g. "plotly_bin_count"
#   the label for the input (in quotes)
    
    ui.input_numeric("px_bin_count", "Bin Count", 10)
    
# Use ui.input_slider() to create a slider input for the number of Seaborn bins
#   pass in four arguments:
#   the name of the input (in quotes), e.g. "seaborn_bin_count"
#   the label for the input (in quotes)
#   the minimum value for the input (as an integer)
#   the maximum value for the input (as an integer)
#   the default value for the input (as an integer)
    ui.input_slider("sns_bin_count", "Sns Bin Count", 1, 100, 10)

# Use ui.input_checkbox_group() to create a checkbox group input to filter the species
#   pass in five arguments:
#   the name of the input (in quotes), e.g.  "selected_species_list"
#   the label for the input (in quotes)
#   a list of options for the input (in square brackets) as ["Adelie", "Gentoo", "Chinstrap"]
#   a keyword argument selected= a list of selected options for the input (in square brackets)
#   a keyword argument inline= a Boolean value (True or False) as you like
    ui.input_checkbox_group("species_selected","Select Species", 
                            ["Adelie", "Gentoo", "Chinstrap"],
                            selected=["Adelie", "Gentoo", "Chinstrap"])
    
# Use ui.a() to add a hyperlink to the sidebar
#   pass in two arguments:
#   the text for the hyperlink (in quotes), e.g. "GitHub"
#   a keyword argument href= the URL for the hyperlink (in quotes), e.g. your GitHub repo URL
#   a keyword argument target= "_blank" to open the link in a new tab
    ui.a("VetterM2 GitHub", "https://github.com/VetterNic/cintel-02-data", target="_blank")



# Display DataTable and Display Data Grid

with ui.layout_columns():
    with ui.accordion(id="accord", open="open"):
        with ui.accordion_panel("DataTable"):
            @render.data_frame
            def vet_penguin_datatable():
                return render.DataTable(penguins_df)
        with ui.accordion_panel("Data Grid"):
            @render.data_frame
            def vet_penguin_data_grid():
                return render.DataGrid(penguins_df)

# Display Histogram with plotly
        
with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Plty Hist"):
        @render_plotly
        def plot():
            plty_hist = px.histogram(
                data_frame=filtered_data(),
                x=input.selected_attribute(),
                nbins=input.px_bin_count(),
                color="species"
            ).update_layout(
                title={"text": "Penguin Mass", "x": 0.5},
                yaxis_title="Count",
                xaxis_title="selected_attribute",
            )
            return plty_hist

# Display Histogram with SNS

    with ui.nav_panel("Sns Hist"):
        @render.plot
        def sns_gram():
            sns_hist = sns.histplot(
                data=filtered_data(),  # Use 'data' instead of 'data_frame'
                x="bill_length_mm",
                bins=input.sns_bin_count())
            sns_hist.set_xlabel("Bill Length") 
            sns_hist.set_ylabel("Count") 
            sns_hist.set_title("Length of Bill")  
            return sns_hist

# Display a plotly scatterplot
    
    with ui.nav_panel("Scatter"):
        @render_plotly
        def plotly_scatterplot():
            scatter_plot = px.scatter(
                data_frame=filtered_data(),
                x="flipper_length_mm",
                y="body_mass_g",
                color="species",
                title="Plotly Scatter: Species",
                labels={"flipper_length_mm": "Flipper Length (mm)", "body_mass_g": "Body Mass (g)"},
                hover_data={"species": True}
            )
            return scatter_plot

@reactive.calc
def filtered_data():
    return penguins_df[
        (penguins_df["species"].isin(input.species_selected()))]

