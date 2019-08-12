#!/usr/bin/python3
#	pystockbalance - Balance stocks in a portfolio
#	Copyright (C) 2019-2019 Johannes Bauer
#
#	This file is part of pystockbalance.
#
#	pystockbalance is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	pystockbalance is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import sys
import json
from FriendlyArgumentParser import FriendlyArgumentParser

parser = FriendlyArgumentParser(description = "Balance multiple asset values to achieve a common divisor ratio.")
parser.add_argument("-s", "--spend-all", action = "store_true", help = "Get rid of all available money.")
parser.add_argument("-a", "--available-money", metavar = "money", type = float, default = 1000000, help = "Available money to buy. Defaults to %(default)s.")
parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
parser.add_argument("filename", metavar = "json_filename", type = str, help = "Problem statement in JSON file form.")
args = parser.parse_args(sys.argv[1:])

with open(args.filename) as f:
	problem = json.load(f)

total_ratio = sum(asset["wanted_ratio"] for asset in problem)
total_value = sum(asset["current_value"] for asset in problem)

for asset in problem:
	current_ratio = asset["current_value"] / total_value
	wanted_ratio = asset["wanted_ratio"] / total_ratio
	print("%20s: value %6.0f want %.1f%% is %.1f%%" % (asset["name"], asset["current_value"], wanted_ratio * 100, current_ratio * 100))

total_buy = 0
available_money = args.available_money
for iteration in range(1000):
	total_deficit_ratio = 0
	deficit_targets = [ ]
	for asset in problem:
		current_ratio = asset["current_value"] / total_value
		wanted_ratio = asset["wanted_ratio"] / total_ratio

		buy_ratio = wanted_ratio - current_ratio
		if buy_ratio > 0:
			total_deficit_ratio += buy_ratio
			deficit_targets.append([ asset, buy_ratio ])
	if len(deficit_targets) == 0:
		break

	deficit_sum = total_deficit_ratio * total_value
	if deficit_sum > available_money:
		deficit_sum = available_money

	for (deficit_asset, deficit_ratio) in deficit_targets:
		buy_sum = deficit_ratio / total_deficit_ratio * deficit_sum
		deficit_asset["current_value"] += buy_sum
		total_value += buy_sum
		total_buy += buy_sum
		available_money -= buy_sum
		deficit_asset["buy"] = deficit_asset.get("buy", 0) + buy_sum

	if available_money < 1:
		break

if (available_money > 1) and args.spend_all:
	for asset in problem:
		wanted_ratio = asset["wanted_ratio"] / total_ratio
		buy_sum = wanted_ratio * available_money
		total_buy += buy_sum
		total_value += buy_sum
		asset["current_value"] += buy_sum
		asset["buy"] = asset.get("buy", 0) + buy_sum

print("~" * 120)
print("Need to spend: %.0f" % (total_buy))
print("~" * 120)
for asset in problem:
	if "buy" not in asset:
		print("%20s: value %6.0f want %.1f%% is %.1f%%" % (asset["name"], asset["current_value"], asset["wanted_ratio"] / total_ratio * 100, asset["current_value"] / total_value * 100))
	else:
		print("%20s: value %6.0f want %.1f%% is %.1f%% after buying %6.0f" % (asset["name"], asset["current_value"], asset["wanted_ratio"] / total_ratio * 100, asset["current_value"] / total_value * 100, asset["buy"]))

