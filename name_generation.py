import numpy as np
from numpy.random import Generator

NOUN_COMBINED_COL = 0
DESCRIPTOR_COMBINED_COL = 0
NOUN_SEPARATE_COL = 1
DESCRIPTOR_SEPARATE_COL = 1
NOUN_PRODUCT_START_COL = 2
DESCRIPTOR_PRODUCT_START_COL = 3
DESCRIPTOR_DECORATOR_ELIGIBLE_COL = 2
DECORATOR_PRODUCT_START_COL = 0

MAX_LETTER_OVERLAP = 0.8

def generate_name(
        attributes : np.ndarray,
        rg : Generator,
        params: tuple
        ) -> tuple[str, int]:

    curr_state = rg.bit_generator.state["state"]["state"]

    attribute_count = attributes.shape[0]

    (   combined_vals,
        decorator_vals,
        noun_array,
        descriptor_array,
        decorator_array,
        noun_list,
        descriptor_list,
        decorator_list
        ) = params

    noun_array = np.array(noun_array)
    descriptor_array = np.array(descriptor_array)
    decorator_array = np.array(decorator_array)

    noun_eligibility = np.full(noun_array.shape[0], True)
    descriptor_eligibility = np.full(descriptor_array.shape[0], True)

    # Determine whether pieces are separate or combined.
    combined = rg.standard_normal()<np.dot(attributes, combined_vals)

    # Winnow down eligibility accordingly. 
    if combined:
        noun_eligibility = noun_eligibility & (noun_array[:, NOUN_COMBINED_COL]==1)
        descriptor_eligibility = descriptor_eligibility & (descriptor_array[:, DESCRIPTOR_COMBINED_COL]==1)
    else:
        noun_eligibility = noun_eligibility & (noun_array[:, NOUN_SEPARATE_COL]==1) 
        descriptor_eligibility = descriptor_eligibility & (descriptor_array[:, DESCRIPTOR_SEPARATE_COL]==1)

    # Select a noun.
    noun_weights = np.dot(attributes, noun_array[:, NOUN_PRODUCT_START_COL:NOUN_PRODUCT_START_COL+attribute_count].T)
    noun_weights[~noun_eligibility] = 0.
    noun_weights = noun_weights / noun_weights.sum()
    noun_index_choice = rg.choice(np.arange(noun_array.shape[0]), p=noun_weights)
    curr_noun = noun_list[noun_index_choice]

    # Select a descriptor. 
    descriptor_weights = np.dot(attributes, descriptor_array[:, DESCRIPTOR_PRODUCT_START_COL:DESCRIPTOR_PRODUCT_START_COL+attribute_count].T)
    descriptor_weights[~descriptor_eligibility] = 0.
    descriptor_weights = descriptor_weights / descriptor_weights.sum()
    descriptor_index_choice = rg.choice(np.arange(descriptor_array.shape[0]), p=descriptor_weights)
    curr_descriptor = descriptor_list[descriptor_index_choice]

    # Check if decorator eligible.
    curr_decorator = ""
    if descriptor_array[descriptor_index_choice, DESCRIPTOR_DECORATOR_ELIGIBLE_COL]==1:
        if rg.standard_normal()<np.dot(attributes, decorator_vals):
            decorator_weights = np.dot(attributes, decorator_array[:, DECORATOR_PRODUCT_START_COL:DECORATOR_PRODUCT_START_COL+attribute_count].T)
            if decorator_weights.sum() > 0:
                decorator_weights = decorator_weights / decorator_weights.sum()
                decorator_index_choice = rg.choice(np.arange(decorator_array.shape[0]), p=decorator_weights)
                curr_decorator = decorator_list[decorator_index_choice]

                # Special case to ensure that we don't end up with double port, fort, etc.
                if (
                    (_overlap_size(curr_decorator.lower(), curr_noun.lower()) > MAX_LETTER_OVERLAP) or
                    (_overlap_size(curr_decorator.lower(), curr_descriptor.lower()) > MAX_LETTER_OVERLAP)
                ):
                    curr_decorator = ""

    # Put it all together.
    result = ""
    if combined:
        result = (curr_descriptor.lower() + curr_noun.lower()).title()
    else:
        result = curr_descriptor.title() + " " + curr_noun.title()

    if curr_decorator != "":
        result = curr_decorator.title() + " " + result

    result = result.replace("'S", "'s").replace(" Of ", " of ")


    return (result, curr_state)

def _overlap_size(word_1 : str, word_2 : str) -> float:
    total_letters = set(word_1) | set(word_2)
    intersecting_letters = set(word_1) & set(word_2)
    return len(intersecting_letters) / len(total_letters)