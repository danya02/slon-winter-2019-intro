# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define b = Character(__("TODO"), image="bot") # TODO: change name

image ship_sunken1 = Movie(play="ship-sunken1.ogv")
image ship_sunken2 = Movie(play="ship-sunken2.ogv")
image ship_sunken3 = Movie(play="ship-sunken3.ogv")
image ship_sunken4 = Movie(play="ship-sunken4.ogv")
image ship_sunken5 = Movie(play="ship-sunken5.ogv")
image ship = "ship noalpha.png"
image cross red = "cross noalpha.png"
image cross white = "cross white noalpha.png"
image empty = "button_empty_hover.png"
image empty white = "button_empty_idle.png"
image bot thinking:
    "bot think1.png"
    pause 0.2
    "bot think2.png"
    pause 0.2
    "bot think3.png"
    pause 0.2
    "bot think4.png"
    pause 0.2
    repeat


init python:
    class Field:
        def __init__(self):
            self.is_ship = False
            self.sunken = False
            self.visible = False
            self.hit = False
            self.highlight=False
    def get_empty_field():
        a=[]
        for i in range(5):
            b = []
            for j in range(5):
                c=Field()
                c.visible=True
                c.hit=False
                b.append(c)
            a.append(b)
        return a
    def get_hidden_field():
        a=[]
        for i in range(5):
            b = []
            for j in range(5):
                c=Field()
                c.hit=False
                b.append(c)
            a.append(b)
        return a

# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show bot happy
    with dissolve

    play music "bgm.mp3"

    # These display lines of dialogue.


    b "Hi there! I'm TODO, and I'd like to welcome you to the game of Battleship!"
    b "This is a two-player game, so you can play with a friend, or, if you'd like, I can play with you!"
    jump choose_action_first

label choose_action_first:
    show bot happy at left
    with move
    menu:
        b "What would you like to do?"
        "Explain the rules.":
            jump rules
        "Play with a person.":
            jump human_play
        "Play with TODO.":
            jump bot_play
        "That's enough for now.":
            jump exit
    jump choose_action_nonfirst

label choose_action_nonfirst:
    show bot happy at left
    with move
    menu:
        b "What would you like to do next?"
        "Explain the rules.":
            jump rules
        "Play with a person.":
            jump human_play
        "Play with TODO.":
            jump bot_play
        "That's enough for now.":
            jump exit
    jump choose_action_nonfirst


label rules:
    show bot happy at right
    with move
    show battleship_board at left
    with dissolve
    b "Battleship is a pencil-and-paper guessing game."
    b "In traditional Battleship, each player has a 10x10 field that they place ships on."
    b "A battleship is a rectangle of length from 1 to 4, but they always have a width of 1."
    b "Ships cannot be touching each other with neither side nor angle, and they must be vertically or horizontally-oriented."
    b "Each player has 1 carrier of length 5, 2 4-long battleships, 7 3-long cruisers and 5 2-long destroyers."
    b "When both players have placed their ships, each player tries to guess where the other person's ships are."
    b "Each player gets a turn, and they select a square on the grid."
    b "The other person tells them whether they hit any ships."
    b "The game ends when either player has hit all of the other person's ships."
    hide battleship_board with dissolve
    show bot happy at center
    with move
    b vhappy "But the rules here are too difficult for some players, so I've simplified them!"
    b happy "The field will be 5x5, and each player has 5 square ships."
    b vhappy "That way, the game will proceed quicker!"
    jump choose_action_nonfirst

init python:
    def test_place_ship(x,y,field):
        try:
            if field[y+1][x].is_ship:return False
        except IndexError:pass
        try:
            if field[y+1][x+1].is_ship:return False
        except IndexError:pass
        try:
            if field[y][x+1].is_ship:return False
        except IndexError:pass
        try:
            if y-1<0:raise IndexError
            if field[y-1][x+1].is_ship:return False
        except IndexError:pass
        try:
            if y-1<0:raise IndexError
            if field[y-1][x].is_ship:return False
        except IndexError:pass
        try:
            if y-1<0:raise IndexError
            if x-1<0:raise IndexError
            if field[y-1][x-1].is_ship:return False
        except IndexError:pass
        try:
            if x-1<0:raise IndexError
            if field[y][x-1].is_ship:return False
        except IndexError:pass
        try:
            if x-1<0:raise IndexError
            if field[y+1][x-1].is_ship:return False
        except IndexError:pass

        return True

    def place_ship(x,y,field):
        field[y][x].is_ship=True
        return True
    def shoot(x,y,field,reffield):
        field[y][x].visible=True
        reffield[y][x].hit=True
        field[y][x].is_ship=reffield[y][x].is_ship
        field[y][x].sunken=reffield[y][x].is_ship
        reffield[y][x].sunken=reffield[y][x].is_ship

        return reffield[y][x].is_ship

    def impossible_place(field):
        positions = []
        for x in range(5):
            for y in range(5):
                positions.append((x,y,))
        for x in range(5):
            for y in range(5):
                if field[y][x].is_ship:
                    for i in [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)]:
                        try:positions.remove(i)
                        except ValueError:pass
        return len(positions)==0



screen gridbutton(x,y,field,reffield,placing,interactive):
    if field[y][x].visible:
        if field[y][x].is_ship:
            if field[y][x].sunken:
                $ sunken_selector = renpy.random.randint(1,5)
                add "ship_sunken[sunken_selector]"
            else:
                add "ship"
        else:
            if placing:
                if test_place_ship(x,y,field):
                    if interactive:
                        imagebutton:
                            auto "button_empty_%s.png"
                            action Function(place_ship,x,y,field)
                    else:
                        add "empty white"
                else:
                    if interactive:
                        imagebutton:
                            idle "cross white noalpha.png"
                            hover "cross noalpha.png"
                            action Notify("You can't place that here.")
                    else:
                        add "cross white"
            else:
                if reffield[y][x].hit:
                    add "cross red"
                else:
                    add "empty white"


    else:
        if interactive:
            imagebutton:
                auto "button_empty_%s.png"
                action Function(shoot,x,y,field,reffield)
        else:
            add "empty white"

screen field_row(y,field,reffield,placing,interactive):
    hbox:
        spacing 10
        use gridbutton(0,y,field,reffield,placing,interactive)
        use gridbutton(1,y,field,reffield,placing,interactive)
        use gridbutton(2,y,field,reffield,placing,interactive)
        use gridbutton(3,y,field,reffield,placing,interactive)
        use gridbutton(4,y,field,reffield,placing,interactive)

screen game_field(field,reffield,placing,interactive):
    vbox:
        spacing 10
        use field_row(0,field,reffield,placing,interactive)
        use field_row(1,field,reffield,placing,interactive)
        use field_row(2,field,reffield,placing,interactive)
        use field_row(3,field,reffield,placing,interactive)
        use field_row(4,field,reffield,placing,interactive)

label human_play:
    show bot happy at center
    with move
    $ p1ships=5
    $ p2ships=5
    $ hit=False
    $ field1 = get_empty_field()
    $ field2 = get_empty_field()
    $ field1see2 = get_hidden_field()
    $ field2see1 = get_hidden_field()

    b "When you're playing with another person, you should not see each other's fields."
    b "For this, I will ask you to pass the device to the other person. No peeping!"
    call switch_1p
    call placement_1p
    call switch_2p
    call placement_2p
    jump human_move_loop


label switch_1p:
    hide game_field
    with dissolve
    show bot happy at center
    with move
    b "Please pass the device to Player 1."
    return
label switch_2p:
    hide game_field
    with dissolve
    show bot happy at center
    with move
    b "Please pass the device to Player 2."
    return

label placement_1p:
    show bot happy at right
    with move
    b "Please place 5 ships on the field."
    window hide dissolve
    $ n=5
    show screen game_field(field1,field1,True,False)
    with dissolve
    hide screen game_field
    while n!=0:
        call screen game_field(field1,field1,True,True)
        $ foobar = impossible_place(field1)
        $ n-=1
        if foobar and n!=0:
            jump placement_error_1p
    window auto
    show screen game_field(field1,field1,True,False)
    pause 1
    hide screen game_field
    with dissolve
    return

label placement_2p:
    show bot happy at right
    with move
    b "Please place 5 ships on the field."
    window hide dissolve
    $ n=5
    show screen game_field(field2,field2,True,False)
    with dissolve
    hide screen game_field
    while n!=0:
        call screen game_field(field2,field2,True,True)
        $ foobar = impossible_place(field2)
        $ n-=1
        if foobar and n!=0:
            jump placement_error_2p
    window auto
    show screen game_field(field2,field2,True,False)
    pause 1
    hide screen game_field
    with dissolve
    return

label placement_error_1p:
    show screen game_field(field1,field1,True,False)
    b surprised "Oh! You can't place another ship, can you?"
    b sad "You should be more careful when placing ships, you know?"
    b "Let's just try placing your ships again, and please be more careful this time."
    hide screen game_field
    with dissolve
    $ field1 = get_empty_field()
    jump placement_1p

label placement_error_2p:
    show screen game_field(field2,field2,True,False)
    b surprised "Oh! You can't place another ship, can you?"
    b sad "You should be careful when placing your ships, you know?"
    b "Let's just try placing your ships again, and please be more careful this time."
    hide screen game_field
    with dissolve
    $ field2 = get_empty_field()
    jump placement_2p

label placement_error_human:
    show screen game_field(field1,field1,True,False)
    window auto
    b "You're taking too long, I'm looking now!"
    b surprised "Oh, there aren't enough ships... but you can't place any more..."
    b sad "Well then, you'll have to start again. Please be more careful this time."
    hide screen game_field
    with dissolve
    $ field1 = get_empty_field()
    jump placement_human


label human_move_loop:
    call switch_1p
    call shoot_1p
    call switch_2p
    call shoot_2p
    jump human_move_loop

label shoot_1p:
    show bot happy at right
    with move
    if hit:
        show screen game_field(field1,field1,False,False)
        with dissolve
        $ hit=False
        b happy "Your opponent has hit one of your ships! You have [p1ships] left!{w=2}{nw}"
        hide screen game_field
        with dissolve
    window hide dissolve
    show screen game_field(field1see2,field2,False,False)
    with dissolve
    hide screen game_field
    call screen game_field(field1see2,field2,False,True)
    if _return:
        $ p2ships-=1
        if p2ships==0:
            jump p1win
        show screen game_field(field1see2,field2,False,False)
        $ hit = True
        b vhappy "You have hit your opponent's ship! [p2ships] left!{w=1}{nw}"
    else:
        show screen game_field(field1see2,field2,False,False)
        b happy "Sorry, but you haven't hit any ships this time.{w=1}{nw}"
    hide screen game_field
    with dissolve
    return

label shoot_2p:
    show bot happy at right
    with move
    if hit:
        show screen game_field(field2,field2,False,False)
        with dissolve
        $ hit=False
        b happy "Your opponent has hit one of your ships! You have [p2ships] left!{w=2}{nw}"
        hide screen game_field
        with dissolve
    window hide dissolve
    show screen game_field(field2see1,field1,False,False)
    with dissolve
    hide screen game_field
    call screen game_field(field2see1,field1,False,True)
    if _return:
        $ p1ships-=1
        if p1ships==0:
            jump p2win
        show screen game_field(field2see1,field1,False,False)
        $ hit = True
        window auto
        b vhappy "You have hit your opponent's ship! [p1ships] left!{w=1}{nw}"
    else:
        show screen game_field(field2see1,field1,False,False)
        window auto
        b happy "Sorry, but you haven't hit any ships this time.{w=1} {nw}"
    hide screen game_field
    with dissolve
    return



label p1win:
    show bot happy at center
    with move
    b "Please share the device."
    b vhappy "Player 1 has won the game!"
    jump choose_action_nonfirst

label p2win:
    show bot happy at center
    with move
    b "Please share the device."
    b vhappy "Player 2 has won the game!"
    jump choose_action_nonfirst

label bot_play:
    show bot vhappy at center
    with move
    b vhappy "So you want to play with me? Great!"
    b blush "Don't worry, I'm not very good..."
    $ p1ships=5
    $ p2ships=5
    $ hit=False
    $ field1 = get_empty_field()
    $ field2 = get_empty_field()
    $ field1see2 = get_hidden_field()
    $ field2see1 = get_hidden_field()
    call placement_human
    call placement_bot
    jump shoot_hb_loop

label shoot_hb_loop:
    call shoot_human
    call shoot_bot
    jump shoot_hb_loop


label placement_human:
    show bot happy at right
    with move
    b "First, you need to place 5 ships on the field."
    b "Don't worry, I won't peek!"
    show bot closed
    window hide dissolve
    $ n=5
    show screen game_field(field1,field1,True,False)
    with dissolve
    hide screen game_field
    while n!=0:
        call screen game_field(field1,field1,True,True)
        $ foobar = impossible_place(field1)
        $ n-=1
        if foobar and n!=0:
            jump placement_error_human
    show screen game_field(field1,field1,True,False)
    window auto
    b "Are you done yet?"
    b "Great!"
    hide screen game_field
    with dissolve
    return
label placement_bot:
    show bot happy at center with move
    b "Now I'll place my ships. Give me a moment...{w=1} {nw}"
    show bot thinking
    python:
        positions=[(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3),(4,4),(0,4),(1,4),(2,4),(3,4)] # outer border of field
        error=True
        while error:
            renpy.random.shuffle(positions)
            toplace=5
            for i in positions:
                if test_place_ship(i[0],i[1],field2):
                    field2[i[1]][i[0]].is_ship = True
                    toplace-=1
                    if toplace==0:
                        error=False
                        break
            if toplace!=0:
                for i in range(32):
                    x=renpy.random.randint(1,3)
                    y=renpy.random.randint(1,3)
                    if test_place_ship(i[0],i[1],field2):
                        field2[i[1]][i[0]].is_ship = True
                        toplace-=1
                        if toplace==0:
                            error=False
                            break

    window hide dissolve
    pause 3
    window auto
    b happy "Done!"
    return

label shoot_human:
    show bot happy at right
    with move
    window hide dissolve
    show screen game_field(field1see2,field2,False,False)
    with dissolve
    hide screen game_field
    call screen game_field(field1see2,field2,False,True)
    if _return:
        $ p2ships-=1
        if p2ships==0:
            jump human_win
        show screen game_field(field1see2,field2,False,False)
        $ hit = True
        window auto
        b "You've hit one of my ships! I've got [p2ships] left! {w=1} {nw}"
    else:
        show screen game_field(field1see2,field2,False,False)
        window auto
        b "You didn't hit any of my ships! {w=1} {nw}"
    hide screen game_field
    with dissolve
    return

label shoot_bot:
    show bot happy at right
    with move
    show screen game_field(field2see1,field1,False,False)
    with dissolve
    show bot thinking
    python:
        s=[__("My turn is..."),__("Let's see..."),__("How about this..."),__("I wonder..."),__("What if I..."),__("How about..."),__("Let's try this...")]
        a=s[renpy.random.randint(1,len(s)-1)]+"{w=1}{nw}"
        renpy.say(b,a)
    pause 2
    python:
        targets_l1=[(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)] # first-importance targets: central 3x3 square
        targets_l2=[(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3),(4,4),(0,4),(1,4),(2,4),(3,4)] # second-importance targets: outer edge
        for x in range(5):
            for y in range(5):
                field2see1[y][x].highlight=True
                if field2see1[y][x].visible:
                    try:targets_l1.remove((x,y))
                    except ValueError:pass
                    try:targets_l2.remove((x,y))
                    except ValueError:pass
                if field2see1[y][x].is_ship:
                    for i in [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)]:
                        try:targets_l1.remove(i)
                        except ValueError:pass
                        try:targets_l2.remove(i)
                        except ValueError:pass
                import time
                field2see1[y][x].highlight=False
        if len(targets_l1)>0:
            target = renpy.random.choice(targets_l1)
        else:
            target = renpy.random.choice(targets_l2)
        _return = shoot(target[0],target[1],field2see1,field1)
        del time


    if _return:
        $ p1ships-=1
        if p1ships==0:
            jump bot_win
        $ hit = True
        window auto
        b vhappy "I hit your ship! You have [p1ships] left, right?"
    else:
        window auto
        $ misses=[__("Aww, I missed..."),__("No hit this time..."),__("Darn it..."),__("No success this time..."),__("Nope, wasn't that...")]
        show bot sad
        $ renpy.say(b,renpy.random.choice(misses)+"{w=1}{nw}")
    hide screen game_field
    with dissolve
    return


label human_win:
    show screen game_field(field1see2,field2,False,False)
    b vhappy "You win! Congratulations!"
    b happy "I told you I'm not very good at this, didn't I?"
    hide screen game_field
    with dissolve
    jump choose_action_nonfirst

label bot_win:
    show screen game_field(field2see1,field1,False,False)
    b vhappy "I win!"
    b happy "Did you have fun?"
    hide screen game_field
    with dissolve
    jump choose_action_nonfirst


label exit:
    show bot happy at center
    with move
    stop music fadeout 10.0
    b "Thank you for playing this game."
    b "I'd like to thank {a=http://unyoe.uunyan.com}unyo@{/a} for providing my sprites, the creator of {a=https://lemmasoft.renai.us/forums/viewtopic.php?t=21515}IIcharacter{/a} for packaging them, {a=https://www.pixiv.net/member.php?id=17385446}VelinquenT{/a} for the background, {a=https://www.emojione.com}EmojiOne{/a} for the icons and {a=https://photomosh.com}Photomosh{/a} for the image distortions."
    b "The music playing in the background is \"Porch Swing Days\" by {a=https://incompetech.com/music}Kevin MacLeod{/a}."
    b vhappy "Thanks for playing!"
    $ renpy.full_restart(transition=Dissolve(0.5))
