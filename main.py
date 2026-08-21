from pyscript import when, web # type: ignore
import name_generation
import json 
import numpy as np

_OPTIONS_SELECTED = ["medium"]*14

@when("click", "#generate-name-btn")
def generate_name(event):

    global _BUTTON_PRESSED
    _BUTTON_PRESSED = True

    attributes = np.full(24, False)

    attributes[0] = True

    attributes[2] = _OPTIONS_SELECTED[0]=="low"
    attributes[3] = _OPTIONS_SELECTED[0]=="high"
    attributes[4] = _OPTIONS_SELECTED[1]=="high"
    attributes[5] = _OPTIONS_SELECTED[1]=="low"
    attributes[6] = _OPTIONS_SELECTED[2]=="high"
    attributes[7] = _OPTIONS_SELECTED[2]=="low"
    attributes[8] = _OPTIONS_SELECTED[3]=="high"
    attributes[9] = _OPTIONS_SELECTED[3]=="low"
    attributes[10] = _OPTIONS_SELECTED[7]=="yes"
    attributes[11] = _OPTIONS_SELECTED[9]=="yes"
    attributes[12] = _OPTIONS_SELECTED[12]=="yes"
    attributes[13] = _OPTIONS_SELECTED[13]=="yes"
    attributes[14] = _OPTIONS_SELECTED[10]=="yes"
    attributes[15] = _OPTIONS_SELECTED[11]=="yes"
    attributes[16] = _OPTIONS_SELECTED[4]=="high"
    attributes[17] = _OPTIONS_SELECTED[4]=="low"
    attributes[18] = _OPTIONS_SELECTED[8]=="yes"
    attributes[19] = _OPTIONS_SELECTED[5]=="high"
    attributes[20] = _OPTIONS_SELECTED[5]=="low"
    attributes[21] = _OPTIONS_SELECTED[6]=="low"
    attributes[22] = _OPTIONS_SELECTED[6]=="high"
    attributes[23] = (not any(attributes[10:17])) & (attributes[5] | attributes[18])
    
    # Gotta fill in that default field if applicable.
    attributes[1] = ~np.any(attributes[2:])

    text, rg_state = name_generation.generate_name(
        attributes,
        rg,
        params )

    # Add the task to the page.
    intro_div = web.page["introduction"]
    intro_div.innerText = "Your settlement's name is"

    output_div = web.page["output"]
    output_div.innerText = text

    rg_div = web.page["rg-state"]
    rg_div.innerText = f"For replicability, the random generator state that created this name was {rg_state}."


def select_option(event, attribute_type, attribute_index):
    global _OPTIONS_SELECTED
    # Find all selection buttons.
    selection_btns = web.page.find(f".selection-btn-{attribute_type}")
    # Remove "selected" styling from all buttons.
    for btn in selection_btns:
        btn.classes.discard("selected")
    # Add "selected" styling to the clicked button.
    event.target.classList.add("selected")
    # Update which selection will be used for new tasks.
    _OPTIONS_SELECTED[attribute_index] = event.target.dataset.selection

@when("click", ".selection-btn-temperature")
def select_option_temperature(event):
    select_option(event, "temperature", 0)

@when("click", ".selection-btn-elevation")
def select_option_elevation(event):
    select_option(event, "elevation", 1)

@when("click", ".selection-btn-latitude")
def select_option_latitude(event):
    select_option(event, "latitude", 2)

@when("click", ".selection-btn-longitude")
def select_option_longitude(event):
    select_option(event, "longitude", 3)

@when("click", ".selection-btn-size")
def select_option_size(event):
    select_option(event, "size", 4)

@when("click", ".selection-btn-wealth")
def select_option_wealth(event):
    select_option(event, "wealth", 5)

@when("click", ".selection-btn-habitability")
def select_option_habitability(event):
    select_option(event, "habitability", 6)

@when("click", ".selection-btn-capital")
def select_option_capital(event):
    select_option(event, "capital", 7)

@when("click", ".selection-btn-island")
def select_option_island(event):
    select_option(event, "island", 8)

@when("click", ".selection-btn-port")
def select_option_port(event):
    select_option(event, "port", 9)

@when("click", ".selection-btn-mine")
def select_option_mine(event):
    select_option(event, "mine", 10)

@when("click", ".selection-btn-arcane")
def select_option_arcane(event):
    select_option(event, "arcane", 11)

@when("click", ".selection-btn-ancient")
def select_option_ancient(event):
    select_option(event, "ancient", 12)

@when("click", ".selection-btn-holy")
def select_option_holy(event):
    select_option(event, "holy", 13)

data = json.load(open("new_sample_grammar.json", "r"))
params = (
    np.array(data["combined_vals"]),
    np.array(data["decorator_vals"]),
    np.array(data["noun_array"]),
    np.array(data["descriptor_array"]),
    np.array(data["decorator_array"]),
    np.array(data["noun_list"]),
    np.array(data["descriptor_list"]),
    np.array(data["decorator_list"]),
)
rg = np.random.default_rng()
