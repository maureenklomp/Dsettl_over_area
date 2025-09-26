

def get_train(i):
    padding = " " * (i % 45)

    # add steam clouds
    steam_length = i % 4
    steam_padding = 12 - (steam_length * 3)

    steam_top = " " * steam_padding + steam_length * "◜◝"
    steam_bottom = " " * steam_padding + steam_length * "◟◞"

    train = (
        f"{padding}{steam_top} \n"
        f"{padding}{steam_bottom} \n"
        f"{padding}  ____   ( )  \n "
        f"{padding} |DD|____T_  \n "
        f"{padding} |_ |_____|<  \n "
        f"{padding}   ⨂-⨂-⨂-oo\\  \n "
    )

    # add turning wheels
    if i % 2 == 0:
        train = train.replace("⨂", "⨁")

    return train