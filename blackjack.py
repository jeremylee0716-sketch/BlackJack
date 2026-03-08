import random


values = {
    '2':2,'3':3,'4':4,'5':5,'6':6,
    '7':7,'8':8,'9':9,'10':10,
    'J':10,'Q':10,'K':10,'A':11
}

ranks = list(values.keys())
suits = ['♠','♥','♦','♣']


def create_deck():
    deck = [r+s for r in ranks for s in suits] * 3
    random.shuffle(deck)
    return deck

def draw_card(shoe):
    if len(shoe) < 50:
        print("\n--- Reshuffling shoe ---")
        shoe = create_deck()

    card = shoe.pop()
    return card, shoe


def score(hand):

    total = 0
    aces = 0

    for card in hand:
        rank = card[:-1]
        total += values[rank]

        if rank == 'A':
            aces += 1

    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total


def ascii_card(card):

    rank = card[:-1]
    suit = card[-1]

    r = rank if len(rank) == 2 else rank + " "

    return [
        "┌─────────┐",
        f"│{r}       │",
        "│         │",
        f"│    {suit}    │",
        "│         │",
        f"│       {r}│",
        "└─────────┘"
    ]


def ascii_hidden():

    return [
        "┌─────────┐",
        "│░░░░░░░░░│",
        "│░░░░░░░░░│",
        "│░░░░░░░░░│",
        "│░░░░░░░░░│",
        "│░░░░░░░░░│",
        "└─────────┘"
    ]


def print_cards(hand, hide_first=False):

    card_lines = []

    for i, card in enumerate(hand):

        if i == 0 and hide_first:
            card_lines.append(ascii_hidden())
        else:
            card_lines.append(ascii_card(card))

    for row in range(7):
        for card in card_lines:
            print(card[row], end=" ")
        print()


def show_table(player, dealer, hide_dealer=True):

    print("\nDealer:")
    print_cards(dealer, hide_dealer)

    if not hide_dealer:
        print("Score:", score(dealer))

    print("\nYou:")
    print_cards(player)
    print("Score:", score(player))


def play_round(shoe):

    player = []
    dealer = []

    card, shoe = draw_card(shoe)
    player.append(card)

    card, shoe = draw_card(shoe)
    dealer.append(card)

    card, shoe = draw_card(shoe)
    player.append(card)

    card, shoe = draw_card(shoe)
    dealer.append(card)

    while True:

        print("\n==============================")
        show_table(player, dealer, True)

        if score(player) > 21:
            print("\nYou bust! Dealer wins.")
            return shoe

        move = input("\nh = hit | s = stand | e = exit : ").lower()

        if move == "e":
            return "exit"

        if move == "h":
            card, shoe = draw_card(shoe)
            player.append(card)

        elif move == "s":
            break


    print("\nDealer's turn")
    show_table(player, dealer, False)

    while score(dealer) < 17:

        input("\nDealer hits... (press enter)")

        card, shoe = draw_card(shoe)
        dealer.append(card)

        show_table(player, dealer, False)


    p = score(player)
    d = score(dealer)

    print("\n==============================")
    print("FINAL RESULT\n")

    show_table(player, dealer, False)

    if d > 21:
        print("\nDealer busts! You win!")

    elif p > d:
        print("\nYou win!")

    elif p < d:
        print("\nDealer wins!")

    else:
        print("\nPush (tie).")

    return shoe


def main():

    shoe = create_deck()

    print("\nBLACKJACK")
    print("3 Deck Shoe")
    print("n = new game | h = hit | s = stand | e = exit\n")

    while True:

        cmd = input("Press n to start a new game or e to exit: ").lower()

        if cmd == "e":
            print("\nThanks for playing!")
            break

        if cmd == "n":

            result = play_round(shoe)

            if result == "exit":
                print("\nThanks for playing!")
                break

            shoe = result


main()