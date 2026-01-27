cons consumable new --name 1984 --type NOVEL
cons c n -n "The Simpsons" -t TV
cons consumable update --name 1984 apply --status IN_PROGRESS --parts 2
cons consumable delete --name 1984
cons consumable list
cons consumable list --order name --reverse
cons consumable list --type NOVEL
cons consumable view --id 1
