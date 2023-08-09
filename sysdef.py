# OpenD10 System Definitions File

# Libraries
from IPython.display import display, Markdown as md
from datetime import date
import pandas as pd
from tabulate import tabulate
import json

# Game Identity

# This code block defines the identity of the game. Here you'll find
# what tiers are called, how many there are, and so on.

tiers = ["NPC", "Novice", "Veteran", "Expert", "Hero"]

with open ("attributes.json", "r") as r:
    attribute_names = json.load(r)

with open ("skills.json", "r") as r:
    skill_names = json.load(r)

with open ("supernatural_classes.json", "r") as r:
    supernatural_classes = json.load(r)

investigation_ranks = [
    "Public",
    "Restricted",
    "Elite",
    "Confidential",
    "Top Secret"]

# --------------------------------------------------------------------------- #

# Game Balance

# This code block contains the general tuning parameters for an implementation
# of OpenD10. This is where you would make adjustments to make an implementation
# more cinematic or realistic, game pacing go faster or slower, and so on.

#                                    -----                                    #

## Core Balance
xp_per_attribute = 10
xp_per_skill = 2
xp_per_supernatural_class = 5
# Design Note: Depending on the technology level of a game, eventually anyone
# can do anything a supernatural can. This parameter adjusts the rarity of
# being supernatural. In a high technology game, this could be adjusted lower...
# and vice versa. Ultimately, this addresses the balance between supernatural
# and mundane PCs. Mundane PCs should be sufficiently more skilled than
# supernatural PCs to not be overshadowed by them.
num_events_per_tier_rating = 5 # So a player spends 5 games in Tier 1,
# 10 games in Tier 2, etc. You can always assign more or less XP depending on
# the pacing desired in a campaign.
credits_per_xp = 1000
# Design Note: We're treating credits as another form of XP. This means that
# there can be features to swap between them. This also means that when a session
# ends, you should account for credits as part of the XP given. You could give
# the session rewards as all XP, as all credits, or a mix. The actual value
# is just to scale credits, but at small values this can affect rounding.

#                                    -----                                    #

## Gear and Ability Balance
gear_discount = 0.1 # This is a discount on abilities that can be lost, stolen, broken, etc.
temp_buff_per_xp = 5 # How much of a bonus each XP grants in an ability

#                                    -----                                    #

## Feature Balance

# The next set of discounts apply to the cost of features based on how often 
# those features are likely to be used. Features that are always useful are 
# not discounted. 
common_feat_discount = 0.5
seldom_feat_discount = 0.66
rare_feat_discount = 0.75
scarce_feat_discount = 0.9

#                                    -----                                    #

## Character Creation
starting_attributes = 25 * len(attribute_names)
attributes_per_tier = 25
# Design Note: These two attributes determine how capable NPCs and PCs generally
# are in the game universe.
starting_max_attribute = 30
max_attributes_per_tier = 5 # Raises the maximum value of an attribute per tier
starting_skills = 2 * len(skill_names)
skills_per_tier = 3 * len(skill_names)
# Design Note: These parameters adjust the probability that a given PC can
# accomplish a given difficulty in a game. With the base roll being a d100,
# lower values mean chance plays more of a role in determining success and
# higher values favor the PC's stats more than the dice roll.

#                                    -----                                    #

## Investigation Balance
weight_per_rating = 10
# This affects how much a PC having contacts or resources contributes to the
# progress of investigation scenes. Lower values highlight the PCs' skills more.

#                                    -----                                    #

## Combat Balance
xp_per_dmg_rating = 10
# Design Note: Amusingly, this value is the basic balance of energy in the
# universe modeled by a TTPRG. Lower values mean that energy is more readily
# available in the game. Weapons will be cheaper and more deadly, vehicles
# will be easier to obtain, and so on.
xp_per_PB_range = 0.125
xp_per_S_range = 0.25
xp_per_M_range = 2.5
xp_per_L_range = 40
smallest_scale = 0.25 # in cm for this game
scale_scalar = 2
item_modification_limit = 5
mod_difficulty_per_mod = 10
mod_time_scalar = 5
mod_cost_scalar = 5
# The primary way PCs improve their abilities is to modify their current ones and
# eventually getting access to better ones. These ultimately relate to the feeling
# of progress and high science/fantasy you want to achieve in your game.
secs_per_round = 6
low_light = 25 # penalty to attack rolls in low light
no_light = 50 # penalty to attack rolls without light

#                                    -----                                    #

## Supernatural Balance
xp_to_ghost = 50 # This relates to the cost of being a ghost, but also
                 # teleportation and scrying costs
mp_burn_discount = 0.1 # This is the discount on abilities that permanently
                 # reduce the PC's mana pool, like essence loss for cybernetic
                 # implants.
subtle_spell_tax = 0.1 # This is a tax on abilities that cannot be countered,
                 # such as psychic abilities or casting without somatic tells.
permanent_gifted_scalar = 25 # This is multiplied by the spell's cost to make it permanent.

# --------------------------------------------------------------------------- #

# Pricer Functions
# These functions will help us use the balancing values above to price
# abilities on the common basis of experience points (XP).

def melee_pricer(die_code,pips):
    price = ((die_code * xp_per_dmg_rating) + (pips * xp_per_dmg_rating / 5.5))
    return price

def ranged_pricer(die_code,pips, PB, S, M, L):
    price = ((die_code * xp_per_dmg_rating) +
             (pips * xp_per_dmg_rating / 5.5) +
             ((300 - PB)/100 * xp_per_PB_range) +
             ((300 - S)/100 * xp_per_S_range) +
             ((300 - M)/100 * xp_per_M_range) +
             ((300 - L)/100 * xp_per_L_range))
    return price

def buff_pricer(amount):
    price = (amount / temp_buff_per_xp)
    return price

def spell_report (cost):
    return (f"Costs {round(cost)} experience points to learn, {round(cost/2)} mana points per use.")