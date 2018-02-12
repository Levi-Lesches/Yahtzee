from random import randint as random
from my_mod import veripy, consecutivipy

score = 0

def print_list (List): 
	temp = ""
	for index, element in enumerate (List):
		temp += str (element) + ", " if index != len (List) - 1 else str (element) + "."
	return (temp)

# Sanitize input of scoring type
score_options_text = "ones (1), twos (2), threes (3), fours (4), fives (5), sixes (6), three of a kind (3oak), four of a kind (4oak), full house (full), small straight (small), large straight (large), yahtzee, chance"
abbreviations = ["1", "2", "3", "4", "5", "6", "3oak", "4oak", "full", "small", "large"]
score_options = ["ones", "twos", "threes", "fours", "fives", "sixes", "three of a kind", "four of a kind", "full house", "small straight", "large straight", "yahtzee", "chance"]


# dice = [1,1,1,1,2]
while len (score_options) > 0:
	print ()
	dice = sorted ([random (1, 6) for x in range (5)])
	print (print_list (dice))
	# check if dice should be re-rolled
	for retry in range (3):
		for die in range (5):
			if veripy (bool, "Reroll %s?" % dice [die]):dice[die]=random (1, 6)
		print ("\n" + print_list (sorted (dice)))

	score_option = veripy (str, "What do you want to score by?", score_options + abbreviations, "Please choose: " + print_list (score_options)).lower()
	# Assign score
	if score_option in score_options [:6]:
		magic_number = score_options.index (score_option) + 1 
		score += dice.count (magic_number) * magic_number
	elif score_option in [str (n) for n in range (1,7)]: score += dice.count (int (score_option)) * int (score_option)
	elif score_option in ["large straight", "large"] and consecutivipy (dice): score += 40
	elif score_option in ["small straight", "small"] and (consecutivipy (dice [:4]) or consecutivipy (dice [1:])): score += 30 
	elif score_option in ["full house", "full"]:
		three_of = None
		pair_of = None
		three_of_a_kind = False
		pair = False
		for die in dice:
			if dice.count (die) == 3 and die not in [three_of, pair_of]:
				three_of_a_kind = True
				three_of = die
				break
		for die in dice:
			if dice.count (die) == 2 and die not in [three_of, pair_of]:
				pair_of = die
				pair = True
				break
		if three_of_a_kind and pair: score += 25
	elif score_option == "yahtzee":
		for number in range (6):
			if all (die == number + 1 for die in dice): score += 50
	elif score_option == "chance": score += sum (dice)
	else:
		for die in dice:
			if score_option in ["three of a kind", "3oak"]:
				if dice.count (die) >= 3:
					score += sum (dice)
					break
			elif score_option in ["four of a kind", "4oak"]:
				if dice.count (die) >= 4:
					score += sum (dice)
					break

	# Remove the scoring type from the main list
	if score_option not in score_options: 
		score_options.pop (abbreviations.index (score_option))
		abbreviations.remove (score_option)
	else:
		abbreviations.pop (score_options.index (score_option))
		score_options.remove (score_option)

	print ()
	if len (score_options) == 0:
		print ("Your final score is: %s." % str (score))
	else:
		print ("Your score so far is: %s." % str (score))
		print ("Choices left: " + print_list (score_options))